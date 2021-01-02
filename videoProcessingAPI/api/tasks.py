import time
import os

from celery import shared_task
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

from django.conf import settings

from api import videoProcessingUtils
from api import misc
from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel
from api.serializers import VideoFileSerializer, SrtFileSerializer, ChunkSerializer


@shared_task(bind=True)
def split_video_celery(self, id):
    start = time.time()

    videoFile = VideoModel.objects.get(id=id)
    videoInstance = videoProcessingUtils.VideoClip(videoFile.path)

    pathToOnlyAudioDir, pathToOnlyVideoDir = misc.create_audio_video_dirs()
    # VideoFileClip from moviepy.editor
    onlyAudioPath, onlyVideoPath = misc.extract_video_audio_seperately_save(
        id, videoInstance, pathToOnlyAudioDir, pathToOnlyVideoDir
    )
    videoToBeSplittedIntoChunks = VideoFileClip(onlyVideoPath)
    audioToBeSplittedIntoChunks = AudioSegment.from_mp3(onlyAudioPath)

    misc.create_dirs_for_splits(id)

    srtFile = SrtModel.objects.get(id=id)
    srtInstance = videoProcessingUtils.SRT(srtFile.path)
    srtData = srtInstance.extractSrtData()

    misc.split_by_chunk(
        id,
        srtData,
        videoToBeSplittedIntoChunks,
        audioToBeSplittedIntoChunks,
        videoFile,
    )
    # fetching data from db.
    videoInstance = VideoModel.objects.get(pk=id)
    chunks = videoInstance.rel.all()
    serializeChunk = misc.serializeObject(ChunkSerializer, chunks, many=True)

    misc.clean_up_dirs(srtFile.path, videoFile.path)
    # building response object
    message = {
        "operationId": id,
        "message": "success",
        "timeTaken": f"{time.time() - start}",
        "path": f"/api/getdetails/{id}",
        "downloadUrl": f"/api/download/{id}",
        "chunks": serializeChunk.data,
    }

    return message


@shared_task(bind=True)
def process_and_generate_final_video_celery(self, operationId):
    bashFiles_path = settings.MEDIA_ROOT + "bashFiles"
    misc.createDirectoryIfNotExists(bashFiles_path)
    # creating directory to bashFiles with operationId as name
    id_as_dir_name = bashFiles_path + f"/{operationId}/"
    try:
        misc.removeAndCreateDirectoryInSamePath(id_as_dir_name)
        chunks = Chunk.objects.all().filter(operationId=operationId)

        audi_file_path = f"{bashFiles_path}/{operationId}/{operationId}AUDI.txt"
        vid_file_path = f"{bashFiles_path}/{operationId}/{operationId}VID.txt"

        (
            merged_audio_destination_path,
            merged_video_destination_path,
        ) = misc.get_merged_destination_paths(operationId)

        final_download_path = settings.MEDIA_ROOT + "downloadable/"
        misc.createDirectoryIfNotExists(final_download_path)

        # check to see if files already exist if exists remove it
        # removeAndCreateDirectoryInSamePath(merged_audio_destination_path,create=False)

        # if os.path.exists(merged_audio_destination_path):
        #     os.remove(merged_audio_destination_path)

        misc.clean_up_dirs(merged_audio_destination_path)

        misc.writePathsToTxtFileToUseWithFFMPEG(chunks, audi_file_path, vid_file_path)

        # use the above files to combne audios and videos
        videoProcessingUtils.mergeAudiosForDownload(
            audi_file_path, merged_audio_destination_path
        )
        videoProcessingUtils.mergeVideoForDownload(
            vid_file_path, merged_video_destination_path
        )

        if not os.path.exists(merged_audio_destination_path) and not os.path.exists(
            merged_video_destination_path
        ):
            return {
                {
                    "message": "failed to create bash ffmpeg comand file",
                }
            }

        videoProcessingUtils.mergeVideoAndAudioToGetDownloadFile(
            operationId,
            merged_video_destination_path,
            merged_audio_destination_path,
            final_download_path,
        )

        # save path of final downloadable file in db
        videoInstance = VideoModel.objects.get(pk=operationId)
        result = FusedResult(
            operationId=videoInstance,
            videoPath=f"{final_download_path}{operationId}.mp4",
            videoName=f"{operationId}VIDEO.mp4",
            videoUrl=settings.MEDIA_URL + f"downloadable/{operationId}.mp4",
        )
        result.save()

        return {
            "message": "combined all video and audio chunk into one file",
            "name_of_file": result.videoName,
            "download": result.videoUrl,
        }

    except:
        return {"message": "Error occured while processing."}
