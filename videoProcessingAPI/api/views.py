# python core modules
import time
import datetime

# 3rd party libraries
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

# django imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel
from api.serializers import VideoFileSerializer, SrtFileSerializer, ChunkSerializer
from django.shortcuts import redirect
from django.conf import settings

# imports for video manipulation
from api import videoProcessingUtils
from api import misc


@api_view(["POST"])
def upload_files_to_server(request):

    if request.method == "POST":
        serializeVideo, serializeSrt = misc.handleUploadedFilesAndSave(request)
        message = {
            "operationId": serializeVideo.data["id"],
            "message": "files uploaded successfully",
            "operation_url": f"/api/process/{serializeVideo.data['id']}",
        }

    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_video_details(request, id):
    if request.method == "GET":
        video = VideoModel.objects.get(pk=id)
        chunks = video.rel.all()
        serializeChunk = ChunkSerializer(chunks, many=True)
        message = {
            "message": "success",
            "downloadUrl": f"/api/download/{id}",
            "chunks": serializeChunk.data,
        }

        return Response(message, status=status.HTTP_200_OK)


@api_view(["GET"])
def split_video(request, id):
    if request.method == "GET":
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
            "message": "success",
            "time(sec)": f"Time: {time.time() - start}",
            "path": f"/api/getdetails/{id}",
            "downloadUrl": f"/api/download/{id}",
            "chunks": serializeChunk.data,
        }

        return Response(message, status=status.HTTP_200_OK)


@api_view(["POST"])
def reupload_audio_chunk(request, chunk_id):
    if request.method == "POST":
        # upload reuploaded audio chunk and resize it.
        try:
            chunk = Chunk.objects.get(pk=chunk_id)
        except:
            return Response({"message": "cannot retrieve from database"})
        # remove files already present for uploading those files again.
        # we can only reupload audio files
        remove_file_path_1 = (
            settings.MEDIA_ROOT + f"audioSplit/{chunk.operationId}/{chunk.me}.mp3"
        )
        remove_file_path_2 = settings.MEDIA_ROOT + f"re-uploads/{chunk.id}.mp3"

        misc.clean_up_files(remove_file_path_1, remove_file_path_2)
        audioInstance = AudioModel(
            audio=request.FILES["file"],
            path=os.path.join(settings.MEDIA_ROOT, f"re-uploads/{chunk_id}.mp3"),
        )
        audioInstance.save()
        length_of_audio_chunk = videoProcessingUtils.getVideoLengthInSeconds(
            chunk.endTime, chunk.startTime
        )
        audio_chunk_save_path = settings.BASE_DIR + chunk.audioChunkPath
        audio_chunk_path = settings.MEDIA_ROOT + f"re-uploads/{chunk_id}.mp3"
        videoProcessingUtils.trimAudioClipAndSave(
            audio_chunk_path, 0, length_of_audio_chunk, audio_chunk_save_path
        )
        return redirect(f"/api/getdetails/{chunk.operationId}")


@api_view(["GET"])
def process_and_generate_final_video(request, operationId):
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
            return Response(
                {
                    "message": "failed to create bash ffmpeg comand file",
                }
            )

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

        response = Response(
            {
                "message": "combined all video anc audio chunk into one file",
                "name_of_file": result.videoName,
                "download": result.videoUrl,
            },
            status=status.HTTP_200_OK,
        )

    except:
        response = Response(
            {"message": "Error occured while processing."},
            status=status.HTTP_409_CONFLICT,
        )

    return response
