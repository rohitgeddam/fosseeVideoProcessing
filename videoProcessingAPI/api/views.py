

#django imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import VideoModel ,SrtModel ,Chunk,FusedResult,AudioModel
from api.serializers import VideoFileSerializer,SrtFileSerializer,ChunkSerializer
from django.shortcuts import  redirect
from django.conf import settings

# python core modules
import os
import shutil
import time
import subprocess
import datetime



#imports for video manipulation
from api.videoProcessing import videoProcessingUtils
import pysrt
from pydub import AudioSegment
from moviepy.editor import *


def checkExtensionOfFileFromRequestObject(requestObject,nameOfField,extension):
    return requestObject.FILES[nameOfField].name.endswith(extension)


def handleUploadedFilesAndSave(request):

    listOfResponses = {
        "fieldRequired" : Response({
            "message": "Field is Required"},
            status=status.HTTP_400_BAD_REQUEST
        ),

        "invalidFileFormat" : Response({
            'message': "invalid file type/s",},
            status=status.HTTP_400_BAD_REQUEST
        ),
    }

    try:
        videoInstance = VideoModel(video=request.FILES['video'],path=os.path.join(settings.MEDIA_ROOT,f"videos/{request.FILES['video'].name}"))
        srtInstance = SrtModel(srt=request.FILES['srt'], path=os.path.join(settings.MEDIA_ROOT,f"srts/{request.FILES['srt'].name}"))
    except:
        return listOfResponses['fieldRequired']

    if checkExtensionOfFileFromRequestObject(request, "video", ".mp4") and checkExtensionOfFileFromRequestObject(request, "srt", ".srt"):
        pass
    else:
        return listOfResponses['invalidFileFormat']

    videoInstance.save()
    srtInstance.save()

    serializeVideo = serializeObject(VideoFileSerializer,videoInstance)
    serializeSrt =  serializeObject(SrtFileSerializer,srtInstance)


    return (serializeVideo,serializeSrt)



def serializeObject(serializerClass,objectToSerialize,many=False):
    return serializerClass(objectToSerialize,many=many)


@api_view(['POST'])
def uploadFilesToServer(request):

    if request.method == 'POST':
        serializeVideo,serializeSrt = handleUploadedFilesAndSave(request)
        message = {
            'operationId': serializeVideo.data['id'],
            "message": "files uploaded successfully",
            "operation_url": f"/api/process/{serializeVideo.data['id']}"
        }

    return Response(message)


@api_view(['GET'])
def getVideoDetails(request, id):
    if request.method == 'GET':
        video = VideoModel.objects.get(pk=id)
        chunks = video.rel.all()
        serializeChunk = ChunkSerializer(chunks, many=True)
        message = {
            "message" : "success",
            "downloadUrl": f"/api/download/{id}",
            "chunks" : serializeChunk.data,
        }

        return Response(message,status=status.HTTP_200_OK)

@api_view(['GET'])
def getListOfPreviouslyProcessedVideos(request):
  if request.method == 'GET':
        videos = VideoModel.objects.all()
        srts = SrtModel.objects.all()
        serializeVideo = serializeObject(VideoFileSerializer,videos,many=True)
        serializeSrt =   serializeObject(SrtFileSerializer,srts,many=True)
        message = {
            # "operationId" : serializeVideo.data['id'],
            "video" : serializeVideo.data,
            "srt" : serializeSrt.data,
        }


def createDirectoryIfNotExists(pathToDirectory,dirName=''):

    pathToCheckFor = pathToDirectory + dirName
    if not os.path.exists(pathToCheckFor):
        os.makedirs(pathToCheckFor)
    return pathToCheckFor


def splitAudioAndVideoIntoChunk(videoToSplit,audioToSplit, chunkData):
    splitedVideoChunk = videoToSplit.subclip(
            videoProcessingUtils.convertTimeToSeconds(chunkData.start.hours, chunkData.start.minutes,
                                                      chunkData.start.seconds, chunkData.start.milliseconds),
            videoProcessingUtils.convertTimeToSeconds(chunkData.end.hours, chunkData.end.minutes,
                                                      chunkData.end.seconds,
                                                      chunkData.end.milliseconds))

    splitedAudioChunk = audioToSplit[
                 videoProcessingUtils.convertTimeToSeconds(chunkData.start.hours, chunkData.start.minutes, chunkData.start.seconds,
                                                           chunkData.start.milliseconds) * 1000:videoProcessingUtils.convertTimeToSeconds(
                     chunkData.end.hours,
                     chunkData.end.minutes,
                     chunkData.end.seconds,
                     chunkData.end.milliseconds) * 1000]

    return splitedVideoChunk,splitedAudioChunk

@api_view(['GET'])
def splitVideo(request, id):
    if request.method == "GET":
        start = time.time()
        try:
            videoFile = VideoModel.objects.get(id=id)
            # fetch srt location by id
            srtFile = SrtModel.objects.get(id=id)
        except:
            return Response({
                "message": "Matching query dosen't exist"
            })

        #open srt file
        srtInstance = videoProcessingUtils.SRT(srtFile.path)
        videoInstance = videoProcessingUtils.VideoClip(videoFile.path)

        pathToOnlyAudioDir = createDirectoryIfNotExists(settings.MEDIA_ROOT,"onlyAudio")
        onlyAudioPath = videoInstance.extractAudioFromVideoAndSave(pathToOnlyAudioDir, f'{id}.mp3')

        pathToOnlyAudioDir = createDirectoryIfNotExists(settings.MEDIA_ROOT,"videoWithoutAudio")
        onlyVideoPath = videoInstance.removeAudioFromVideoAndSave(pathToOnlyAudioDir, f'{id}.mp4')

        videoToBeSplittedIntoChunks = VideoFileClip(onlyVideoPath)
        audioToBeSplittedIntoChunks = AudioSegment.from_mp3(onlyAudioPath)

        pathToStoreChunksOfSplitedVideo = settings.MEDIA_ROOT + f'videoSplit/{id}'
        pathToStoreChunksOfSplitedAudio = settings.MEDIA_ROOT + f'audioSplit/{id}'

        createDirectoryIfNotExists(pathToStoreChunksOfSplitedVideo)
        createDirectoryIfNotExists(pathToStoreChunksOfSplitedAudio)

        srtData = srtInstance.extractSrtData()


        # i is a counter variable
        i = 1
        for chunk in srtData:
            try:

                videoPart,audioPart = splitAudioAndVideoIntoChunk(videoToBeSplittedIntoChunks,audioToBeSplittedIntoChunks,chunk)

                videoChunkPath = settings.MEDIA_ROOT + f'/videoSplit/{id}/{i}.mp4'
                audioChunkPath = settings.MEDIA_ROOT + f'/audioSplit/{id}/{i}.mp3'
                #saving video cunk
                videoPart.write_videofile(videoChunkPath )
                #saving audio chunk
                audioPart.export(audioChunkPath, format="mp3")

                chunkStartTime = datetime.time(chunk.start.hours,chunk.start.minutes,chunk.start.seconds)
                chunkEndTime = datetime.time(chunk.end.hours,chunk.end.minutes,chunk.end.seconds)


                audioChunkUrlPath = settings.MEDIA_URL + f'audioSplit/{id}/{i}.mp3'
                videoChunkUrlPath = settings.MEDIA_URL + f'videoSplit/{id}/{i}.mp4'

                detailsAboutChunk = Chunk(
                    operationId= videoFile,
                    me = i,
                    videoChunkPath=videoChunkUrlPath,
                    videoChunkName=f'{i}.mp4',
                    audioChunkPath=audioChunkUrlPath,
                    audioChunkName=f'{i}.mp3',
                    subtitleChunk = chunk.text,
                    startTime= chunkStartTime,
                    endTime = chunkEndTime,
                )

                detailsAboutChunk.save()
                i = i + 1

            except ValueError:
                break

        #fetching data from db.
        videoInstance = VideoModel.objects.get(pk=id)
        chunks = videoInstance.rel.all()
        serializeChunk = serializeObject(ChunkSerializer,chunks, many=True)

        #building response object
        message = {
            "message": "success",
            "time(sec)": f'Time: {time.time() - start}',
            "path": f"/api/fetchdetails/{id}",
            "downloadUrl":f"/api/download/{id}",
            "chunks": serializeChunk.data,
        }

        return Response(message, status=status.HTTP_200_OK)





@api_view(['POST'])
def reuploadAudioChunk(request, chunk_id):
    if request.method == 'POST':
        #upload reuploaded audio chunk and resize it.
        chunk = Chunk.objects.get(pk=chunk_id)
        #remove files already present for uploading those files again.
        remove_file_path_1 = settings.MEDIA_ROOT + f"audioSplit/{chunk.operationId}/{chunk.me}.mp3"
        remove_file_path_2 = settings.MEDIA_ROOT + f"re-uploads/{chunk.id}.mp3"
        if os.path.exists(remove_file_path_1):
            os.remove(remove_file_path_1)
        if os.path.exists(remove_file_path_2):
            os.remove(remove_file_path_2)

        audioInstance = AudioModel(audio=request.FILES['file'],path=os.path.join(settings.MEDIA_ROOT,f're-uploads/{chunk_id}.mp3'))
        audioInstance.save()

        length_of_audio_chunk = videoProcessingUtils.getVideoLengthInSeconds(chunk.endTime, chunk.startTime)
        audio_chunk_save_path = settings.BASE_DIR  + chunk.audioChunkPath
        audio_chunk_path = settings.MEDIA_ROOT +f"re-uploads/{chunk_id}.mp3"

        videoProcessingUtils.trimVideoClipAndSave(audio_chunk_path, 0, length_of_audio_chunk, audio_chunk_save_path)

        return redirect(f"/api/fetchdetails/{chunk.operationId}")


def removeAndCreateDirectoryInSamePath(dirPath,create=True):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)
    if create==True:
        os.mkdir(dirPath)



def writePathsToTxtFileToUseWithFFMPEG(chunks,audioFilePath,videoFilePath):
    audiFile = open(audioFilePath, 'a')
    vidFile = open(videoFilePath, 'a')
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



@api_view(['GET'])
def processAndGenerateFinalVideo(request,operationId):
    bashFiles_path = settings.MEDIA_ROOT + "bashFiles"
    #creating directory to bashFiles with operationId as name
    id_as_dir_name = bashFiles_path + f"/{operationId}/"

    # try:
    removeAndCreateDirectoryInSamePath(id_as_dir_name)
    chunks = Chunk.objects.all().filter(operationId=operationId)


    audi_file_path = f"{bashFiles_path}/{operationId}/{operationId}AUDI.txt"
    vid_file_path = f"{bashFiles_path}/{operationId}/{operationId}VID.txt"

    merged_audio_destination_path = settings.MEDIA_ROOT+f"audioSplit/{operationId}/mergedAUDIO.mp3"
    merged_video_destination_path = settings.MEDIA_ROOT+f"videoSplit/{operationId}/mergedVIDEO.mp4"

    path__to_final_downloadable = settings.MEDIA_ROOT + "downloadable/"

    # check to see if files already exist if exists remove it
    # removeAndCreateDirectoryInSamePath(merged_audio_destination_path,create=False)

    if os.path.exists(merged_audio_destination_path):
        os.remove(merged_audio_destination_path)

    writePathsToTxtFileToUseWithFFMPEG(chunks,audi_file_path,vid_file_path)


    # use the above files to combne audios and videos
    videoProcessingUtils.mergeAudiosForDownload(audi_file_path,merged_audio_destination_path)
    videoProcessingUtils.mergeVideoForDownload(vid_file_path,merged_video_destination_path)

    if not os.path.exists(merged_audio_destination_path) and not os.path.exists(merged_video_destination_path):
        return Response({
            "message" : "failed to create bash ffmpeg comand file",
        })

    videoProcessingUtils.mergeVideoAndAudioToGetDownloadFile(operationId,merged_video_destination_path,merged_audio_destination_path,path__to_final_downloadable)

    #save path of final downloadable file in db
    videoInstance = VideoModel.objects.get(pk = operationId)
    result = FusedResult(
        operationId=videoInstance,
        videoPath = f"{path__to_final_downloadable}{operationId}.mp4",
        videoName= f"{operationId}VIDEO.mp4",
        videoUrl= settings.MEDIA_URL + f"downloadable/{operationId}.mp4",
    )
    result.save()

    response = Response({
    "message": "combined all video anc audio chunk into one file",
    "name_of_file" : result.videoName,
    "download" : result.videoUrl
    })
    # except:
    #     response = Response({
    #         "message":"Error occured while processing."
    #     },status=status.HTTP_409_CONFLICT)

    return response