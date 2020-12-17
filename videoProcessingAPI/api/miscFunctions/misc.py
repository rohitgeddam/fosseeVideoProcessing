# python core modules
import shutil

# django imports
from rest_framework import status
from rest_framework.response import Response
from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel
from api.serializers import VideoFileSerializer, SrtFileSerializer, ChunkSerializer
from django.conf import settings

# imports for video manipulation
from api.videoProcessing import videoProcessingUtils
from api.miscFunctions import misc
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
    if create == True:
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