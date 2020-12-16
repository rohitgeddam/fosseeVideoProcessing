# python core modules
import time
import datetime

# 3rd party libraries
from pydub import AudioSegment
from moviepy.editor import *

# django imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel
from api.serializers import VideoFileSerializer, SrtFileSerializer, ChunkSerializer
from django.shortcuts import redirect
from django.conf import settings

# imports for video manipulation
from api.videoProcessing import videoProcessingUtils
from api.miscFunctions import misc


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

        pathToOnlyAudioDir, pathToOnlyVideoDir = create_audio_video_dirs()
        onlyAudioPath, onlyVideoPath = extract_video_audio_seperately_save(
            videoInstance, pathToOnlyAudioDir, pathToOnlyVideoDir
        )
        # VideoFileClip from moviepy.editor
        videoToBeSplittedIntoChunks = VideoFileClip(onlyVideoPath)
        audioToBeSplittedIntoChunks = AudioSegment.from_mp3(onlyAudioPath)

        create_dirs_for_splits()

        srtFile = SrtModel.objects.get(id=id)
        srtInstance = videoProcessingUtils.SRT(srtFile.path)
        srtData = srtInstance.extractSrtData()

        split_by_chunk(
            srtData, videoToBeSplittedIntoChunks, audioToBeSplittedIntoChunks, videoFile
        )
        # fetching data from db.
        videoInstance = VideoModel.objects.get(pk=id)
        chunks = videoInstance.rel.all()
        serializeChunk = misc.serializeObject(ChunkSerializer, chunks, many=True)

        clean_up_dirs(srtFile, videoFile)
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
        remove_file_path_1 = (
            settings.MEDIA_ROOT + f"audioSplit/{chunk.operationId}/{chunk.me}.mp3"
        )
        remove_file_path_2 = settings.MEDIA_ROOT + f"re-uploads/{chunk.id}.mp3"
        while os.path.exists(remove_file_path_1):
            os.remove(remove_file_path_1)
        while os.path.exists(remove_file_path_2):
            os.remove(remove_file_path_2)

        audioInstance = AudioModel(
            audio=request.FILES["file"],
            path=os.path.join(settings.MEDIA_ROOT, f"re-uploads/{chunk_id}.mp3"),
        )
        audioInstance.save()

        length_of_audio_chunk = videoProcessingUtils.getVideoLengthInSeconds(
            chunk.endTime, chunk.startTime
        )
        audio_chunk_save_path = settings.BASE_DIR + chunk.audioChunkPath
        print("MONTSTER_____---------------------")
        print(audio_chunk_save_path)
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

        merged_audio_destination_path = (
            settings.MEDIA_ROOT + f"audioSplit/{operationId}/mergedAUDIO.mp3"
        )
        merged_video_destination_path = (
            settings.MEDIA_ROOT + f"videoSplit/{operationId}/mergedVIDEO.mp4"
        )

        path__to_final_downloadable = settings.MEDIA_ROOT + "downloadable/"
        misc.createDirectoryIfNotExists(path__to_final_downloadable)

        # check to see if files already exist if exists remove it
        # removeAndCreateDirectoryInSamePath(merged_audio_destination_path,create=False)

        if os.path.exists(merged_audio_destination_path):
            os.remove(merged_audio_destination_path)

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
            path__to_final_downloadable,
        )

        # save path of final downloadable file in db
        videoInstance = VideoModel.objects.get(pk=operationId)
        result = FusedResult(
            operationId=videoInstance,
            videoPath=f"{path__to_final_downloadable}{operationId}.mp4",
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


def create_audio_video_dirs():
    pathToOnlyAudioDir = misc.createDirectoryIfNotExists(
        settings.MEDIA_ROOT, "onlyAudio"
    )

    pathToOnlyVideoDir = misc.createDirectoryIfNotExists(
        settings.MEDIA_ROOT, "videoWithoutAudio"
    )
    return (pathToOnlyAudioDir, pathToOnlyVideoDir)


def extract_video_audio_seperately_save(video, pathToOnlyAudioDir, pathToOnlyVideoDir):
    onlyVideoPath = video.removeAudioFromVideoAndSave(pathToOnlyVideoDir, f"{id}.mp4")
    onlyAudioPath = video.extractAudioFromVideoAndSave(pathToOnlyAudioDir, f"{id}.mp3")
    return (onlyAudioPath, onlyVideoPath)


def create_dirs_for_splits():
    pathToStoreChunksOfSplitedVideo = settings.MEDIA_ROOT + f"videoSplit/{id}"
    pathToStoreChunksOfSplitedAudio = settings.MEDIA_ROOT + f"audioSplit/{id}"

    misc.createDirectoryIfNotExists(pathToStoreChunksOfSplitedVideo)
    misc.createDirectoryIfNotExists(pathToStoreChunksOfSplitedAudio)


def split_by_chunk(srtData, video, audio, videoFile):

    i = 1
    for chunk in srtData:
        try:

            videoPart, audioPart = misc.splitAudioAndVideoIntoChunk(video, audio, chunk)

            videoChunkPath = settings.MEDIA_ROOT + f"videoSplit/{id}/{i}.mp4"
            audioChunkPath = settings.MEDIA_ROOT + f"audioSplit/{id}/{i}.mp3"
            # saving video cunk
            videoPart.write_videofile(videoChunkPath)
            # saving audio chunk
            audioPart.export(audioChunkPath, format="mp3")

            chunkStartTime = datetime.time(
                chunk.start.hours, chunk.start.minutes, chunk.start.seconds
            )
            chunkEndTime = datetime.time(
                chunk.end.hours, chunk.end.minutes, chunk.end.seconds
            )
            audioChunkLocalPath, videoChunkLocalPath = get_local_paths_with_i(i)
            audioChunkUrlPath, videoChunkUrlPath = get_url_paths_with_i(i)

            detailsAboutChunk = Chunk(
                operationId=videoFile,
                me=i,
                videoChunkLocalPath=videoChunkLocalPath,
                videoChunkPath=videoChunkUrlPath,
                audioChunkPath=audioChunkUrlPath,
                videoChunkName=f"{i}.mp4",
                audioChunkLocalPath=audioChunkLocalPath,
                audioChunkName=f"{i}.mp3",
                subtitleChunk=chunk.text,
                startTime=chunkStartTime,
                endTime=chunkEndTime,
            )

            detailsAboutChunk.save()
            i = i + 1

        except ValueError:
            break


def get_local_paths_with_i(i):

    audioChunkLocalPath = settings.MEDIA_ROOT + f"audioSplit/{id}/{i}.mp3"
    videoChunkLocalPath = settings.MEDIA_ROOT + f"videoSplit/{id}/{i}.mp4"
    return (audioChunkLocalPath, videoChunkLocalPath)


def get_url_paths_with_i(i):
    audioChunkUrlPath = settings.MEDIA_URL + f"audioSplit/{id}/{i}.mp3"
    videoChunkUrlPath = settings.MEDIA_URL + f"videoSplit/{id}/{i}.mp4"
    return (audioChunkUrlPath, videoChunkUrlPath)


def clean_up_dirs(srtFile, videoFile):
    # deleting original files to save space
    if os.path.exists(srtFile.path):
        os.remove(srtFile.path)
    if os.path.exists(videoFile.path):
        os.remove(videoFile.path)
