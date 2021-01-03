# python core modules
import shutil, os, datetime

# django imports
from django.conf import settings

# imports for video manipulation
from api.models import VideoModel, SrtModel, Chunk
from api.serializers import VideoFileSerializer, SrtFileSerializer
from api import videoProcessingUtils
from api import misc
from moviepy.editor import *


listOfResponses = {
    "fieldRequired": {"message": "Field is Required"},
    "invalidFileFormat": {
        "message": "invalid file type/s",
    },
}


def checkExtensionOfFileFromRequestObject(requestObject, nameOfField, extension):
    """Check file extension from the request object"""

    return requestObject.FILES[nameOfField].name.endswith(extension)


def handleUploadedFilesAndSave(request):
    """Handle uploaded files and save them"""

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
    except Exception:
        return (None, None, listOfResponses["fieldRequired"])

    if misc.checkExtensionOfFileFromRequestObject(
        request, "video", ".mp4"
    ) and misc.checkExtensionOfFileFromRequestObject(request, "srt", ".srt"):
        pass
    else:
        return (None, None, listOfResponses["invalidFileFormat"])

    videoInstance.save()
    srtInstance.save()

    serializeVideo = misc.serializeObject(VideoFileSerializer, videoInstance)
    serializeSrt = misc.serializeObject(SrtFileSerializer, srtInstance)

    return (serializeVideo, serializeSrt, None)


def serializeObject(serializerClass, objectToSerialize, many=False):
    """Serialize object using the provided serializer class"""

    return serializerClass(objectToSerialize, many=many)


def removeAndCreateDirectoryInSamePath(dirPath, create=True):
    """Remove and Create New Directory in the given path"""

    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)
    if create is True:
        os.mkdir(dirPath)


def createDirectoryIfNotExists(pathToDirectory, dirName=""):
    """Create a new directory if the directory dosen't exists"""

    pathToCheckFor = pathToDirectory + dirName
    if not os.path.exists(pathToCheckFor):
        os.makedirs(pathToCheckFor)
    return pathToCheckFor


def splitAudioAndVideoIntoChunk(videoToSplit, audioToSplit, chunkData):
    """Split Audio and Video into chunks"""

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
    """Write file path of audio and video files into a text file
    to use with the FFMPEG commandline utility"""

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
    """Create Audio and Video directories"""

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
    """Save Video And Audio into seperate files"""

    onlyVideoPath = video.removeAudioFromVideoAndSave(pathToOnlyVideoDir, f"{id}.mp4")
    onlyAudioPath = video.extractAudioFromVideoAndSave(pathToOnlyAudioDir, f"{id}.mp3")
    return (onlyAudioPath, onlyVideoPath)


def create_dirs_for_splits(id):
    """Create directories to save the chunks"""

    pathToStoreChunksOfSplitedVideo = settings.MEDIA_ROOT + f"videoSplit/{id}"
    pathToStoreChunksOfSplitedAudio = settings.MEDIA_ROOT + f"audioSplit/{id}"

    misc.createDirectoryIfNotExists(pathToStoreChunksOfSplitedVideo)
    misc.createDirectoryIfNotExists(pathToStoreChunksOfSplitedAudio)


def split_by_chunk(id, srtData, video, audio, videoFile):
    """Split video into chunks using srt file data"""

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
            audioChunkLocalPath, videoChunkLocalPath = get_local_paths_with_i(id, i)
            audioChunkUrlPath, videoChunkUrlPath = get_url_paths_with_i(id, i)

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


def get_local_paths_with_i(id, i):
    """Get the local path with index"""

    audioChunkLocalPath = settings.MEDIA_ROOT + f"audioSplit/{id}/{i}.mp3"
    videoChunkLocalPath = settings.MEDIA_ROOT + f"videoSplit/{id}/{i}.mp4"
    return (audioChunkLocalPath, videoChunkLocalPath)


def get_url_paths_with_i(id, i):
    """Get the Url path with index"""

    audioChunkUrlPath = settings.MEDIA_URL + f"audioSplit/{id}/{i}.mp3"
    videoChunkUrlPath = settings.MEDIA_URL + f"videoSplit/{id}/{i}.mp4"
    return (audioChunkUrlPath, videoChunkUrlPath)


def clean_up_dirs(*args):
    """Delete Directories"""

    # deleting original files to save space
    for path in args:
        if os.path.exists(path):
            os.remove(path)


def clean_up_files(*args):
    """Delete Files"""

    for path in args:
        while os.path.exists(path):
            os.remove(path)


def get_merged_destination_paths(operationId):
    """Get the final video path"""

    audio_path = settings.MEDIA_ROOT + f"audioSplit/{operationId}/mergedAUDIO.mp3"
    video_path = settings.MEDIA_ROOT + f"videoSplit/{operationId}/mergedVIDEO.mp4"
    return (audio_path, video_path)
