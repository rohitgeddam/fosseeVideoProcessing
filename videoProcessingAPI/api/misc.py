# python core modules
import shutil
import os
import datetime

# django imports
from rest_framework import status
from rest_framework.response import Response
from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel
from api.serializers import VideoFileSerializer, SrtFileSerializer, ChunkSerializer
from django.conf import settings

# imports for video manipulation
from api import videoProcessingUtils
from api import misc
from moviepy.editor import *


listOfResponses = {
    "fieldRequired": Response(
        {"message": "Field is Required"}, status=status.HTTP_400_BAD_REQUEST
    ),
    "invalidFileFormat": Response(
        {
            "message": "invalid file type/s",
        },
        status=status.HTTP_400_BAD_REQUEST,
    ),
}


def checkExtensionOfFileFromRequestObject(requestObject, nameOfField, extension):
    return requestObject.FILES[nameOfField].name.endswith(extension)


def handleUploadedFilesAndSave(request):

    try:
        videoInstance = VideoModel(
            video=request.FILES["video"],
            path=os.path.join(
                settings.MEDIA_ROOT, f"videos/{request.FILES['video'].name}"
            ),
        )
        srtInstance = SrtModel(
            srt=request.FILES["srt"],
            path=os.path.join(settings.MEDIA_ROOT, f"srts/{request.FILES['srt'].name}"),
        )
    except:
        return listOfResponses["fieldRequired"]

    if misc.checkExtensionOfFileFromRequestObject(
        request, "video", ".mp4"
    ) and misc.checkExtensionOfFileFromRequestObject(request, "srt", ".srt"):
        pass
    else:
        return listOfResponses["invalidFileFormat"]

    videoInstance.save()
    srtInstance.save()

    serializeVideo = misc.serializeObject(VideoFileSerializer, videoInstance)
    serializeSrt = misc.serializeObject(SrtFileSerializer, srtInstance)

    return (serializeVideo, serializeSrt)


def serializeObject(serializerClass, objectToSerialize, many=False):
    return serializerClass(objectToSerialize, many=many)


def removeAndCreateDirectoryInSamePath(dirPath, create=True):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)
    if create is True:
        os.mkdir(dirPath)


def createDirectoryIfNotExists(pathToDirectory, dirName=""):

    pathToCheckFor = pathToDirectory + dirName
    if not os.path.exists(pathToCheckFor):
        os.makedirs(pathToCheckFor)
    return pathToCheckFor


def splitAudioAndVideoIntoChunk(videoToSplit, audioToSplit, chunkData):
    print("SPLIT", dir(videoToSplit), audioToSplit, "chunk dir ", dir(chunkData))
    splitedVideoChunk = videoToSplit.subclip(
        videoProcessingUtils.convertTimeToSeconds(
            chunkData.start.hours,
            chunkData.start.minutes,
            chunkData.start.seconds,
            chunkData.start.milliseconds,
        ),
        videoProcessingUtils.convertTimeToSeconds(
            chunkData.end.hours,
            chunkData.end.minutes,
            chunkData.end.seconds,
            chunkData.end.milliseconds,
        ),
    )

    splitedAudioChunk = audioToSplit[
        videoProcessingUtils.convertTimeToSeconds(
            chunkData.start.hours,
            chunkData.start.minutes,
            chunkData.start.seconds,
            chunkData.start.milliseconds,
        )
        * 1000 : videoProcessingUtils.convertTimeToSeconds(
            chunkData.end.hours,
            chunkData.end.minutes,
            chunkData.end.seconds,
            chunkData.end.milliseconds,
        )
        * 1000
    ]

    return splitedVideoChunk, splitedAudioChunk


def writePathsToTxtFileToUseWithFFMPEG(chunks, audioFilePath, videoFilePath):
    audiFile = open(audioFilePath, "a")
    vidFile = open(videoFilePath, "a")
    # removeing the last slash as its causing problem
    # -7 to strip last 7 characters in settings.MEDIA_ROOT to avoid repetition.
    media_path = settings.MEDIA_ROOT[:-7]

    for chunk in chunks:
        audio_chunk_path = media_path + chunk.audioChunkPath
        video_chunk_path = media_path + chunk.videoChunkPath
        audiFile.write(f"file '{audio_chunk_path}'\n")
        vidFile.write(f"file '{video_chunk_path}'\n")

    audiFile.close()
    vidFile.close()


def create_audio_video_dirs():
    pathToOnlyAudioDir = misc.createDirectoryIfNotExists(
        settings.MEDIA_ROOT, "onlyAudio"
    )

    pathToOnlyVideoDir = misc.createDirectoryIfNotExists(
        settings.MEDIA_ROOT, "videoWithoutAudio"
    )

    return (pathToOnlyAudioDir, pathToOnlyVideoDir)


def extract_video_audio_seperately_save(
    id, video, pathToOnlyAudioDir, pathToOnlyVideoDir
):

    onlyVideoPath = video.removeAudioFromVideoAndSave(pathToOnlyVideoDir, f"{id}.mp4")
    onlyAudioPath = video.extractAudioFromVideoAndSave(pathToOnlyAudioDir, f"{id}.mp3")
    # print("AUDviD", onlyAudioPath, onlyVideoPath)
    return (onlyAudioPath, onlyVideoPath)


def create_dirs_for_splits(id):
    pathToStoreChunksOfSplitedVideo = settings.MEDIA_ROOT + f"videoSplit/{id}"
    pathToStoreChunksOfSplitedAudio = settings.MEDIA_ROOT + f"audioSplit/{id}"

    misc.createDirectoryIfNotExists(pathToStoreChunksOfSplitedVideo)
    misc.createDirectoryIfNotExists(pathToStoreChunksOfSplitedAudio)


def split_by_chunk(id, srtData, video, audio, videoFile):
    i = 1
    for chunk in srtData:
        try:
            videoPart, audioPart = misc.splitAudioAndVideoIntoChunk(video, audio, chunk)
            videoChunkPath = settings.MEDIA_ROOT + f"videoSplit/{id}/{i}.mp4"
            audioChunkPath = settings.MEDIA_ROOT + f"audioSplit/{id}/{i}.mp3"
            # saving video cunk
            try:
                videoPart.write_videofile(videoChunkPath)
            except TypeError:
                print("Error occured while writing video file to directory")
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
            raise ValueError("ERROR OCCURED WHILE SPLITTING BY CHUNKS")
            break


def get_local_paths_with_i(i):

    audioChunkLocalPath = settings.MEDIA_ROOT + f"audioSplit/{id}/{i}.mp3"
    videoChunkLocalPath = settings.MEDIA_ROOT + f"videoSplit/{id}/{i}.mp4"
    return (audioChunkLocalPath, videoChunkLocalPath)


def get_url_paths_with_i(i):
    audioChunkUrlPath = settings.MEDIA_URL + f"audioSplit/{id}/{i}.mp3"
    videoChunkUrlPath = settings.MEDIA_URL + f"videoSplit/{id}/{i}.mp4"
    return (audioChunkUrlPath, videoChunkUrlPath)


def clean_up_dirs(*args):
    # deleting original files to save space
    for path in args:
        if os.path.exists(path):
            os.remove(path)


def clean_up_files(*args):
    for path in args:
        while os.path.exits(path):
            os.remove(path)


def get_merged_destination_paths(operationId):
    audio_path = settings.MEDIA_ROOT + f"audioSplit/{operationId}/mergedAUDIO.mp3"
    video_path = settings.MEDIA_ROOT + f"videoSplit/{operationId}/mergedVIDEO.mp4"
    return (audio_path, video_path)
