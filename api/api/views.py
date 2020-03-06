

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
        videoInstance = VideoModel(video=request.FILES['video'],path=os.path.join(settings.MEDIA_ROOT))
        srtInstance = SrtModel(srt=request.FILES['srt'], path=os.path.join(settings.MEDIA_ROOT))
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



@api_view(['GET'])
def split_video(request,id):
    if request.method == "GET":
        start = time.time()
        try:
            # fetch video location by id
            videoFile = VideoModel.objects.get(id=id)
            # fetch srt location by id
            srtFile = SrtModel.objects.get(id=id)
        except:
            return Response({
                "message": "Matching query dosen't exist"
            })

        # print(os.path.join(settings.MEDIA_ROOT, videoFile.path))


        #open srt file
        srt = videoProcessingUtils.SRT(settings.MEDIA_ROOT + srtFile.path)

        video = videoProcessingUtils.VideoClip(settings.MEDIA_ROOT + videoFile.path)

        # onlyAudioPath = video.extractAudio(os.path.join(settings.MEDIA_ROOT,'onlyAudio'),f'{id}.mp3')
        onlyAudioPath = video.extractAudioFromVideoAndSave(settings.MEDIA_ROOT + 'onlyAudio', f'{id}.mp3')


        # print(onlyAudioPath)
        onlyVideoPath = video.removeAudioFromVideoAndSave(settings.MEDIA_ROOT + 'videoWithoutAudio', f'{id}.mp4')

        videoToSplit = VideoFileClip(onlyVideoPath)
        audioToSplit = AudioSegment.from_mp3(onlyAudioPath)
        #

        videoSplitPath = settings.MEDIA_ROOT + f'videoSplit/{id}'
        audioSplitPath = settings.MEDIA_ROOT + f'audioSplit/{id}'
        # if not os.path.exists(videoSplitPath):
        #     os.makedirs(videoSplitPath)
        # else:
        #     shutil.rmtree(videoSplitPath)  # Removes all the subdirectories!
        #     os.makedirs(videoSplitPath)
        #
        # if not os.path.exists(audioSplitPath):
        #     os.makedirs(audioSplitPath)
        # else:
        #     shutil.rmtree(audioSplitPath)  # Removes all the subdirectories!
        #     os.makedirs(audioSplitPath)

        if not os.path.exists(videoSplitPath) and not os.path.exists(audioSplitPath):
            os.makedirs(videoSplitPath)
            os.makedirs(audioSplitPath)
        else:
            return Response({
                "message" : "operation already performed on this ID",
                "view details" : f"/api/fetchdetails/{id}",
                "downloadUrl":f"/api/download/{id}",
            })
            # return redirect(f'fetchdetails/{id}')
        srtData = srt.extractSrtData()
        subData = []
        i = 1
        for chunk in srtData:
            # command = f"mencoder -ss {chunk.start.hours}:{chunk.start.minutes}:{chunk.start.seconds}.{chunk.start.milliseconds} -endpos {chunk.end.hours}:{chunk.end.minutes}:{chunk.end.seconds}.{chunk.end.milliseconds} -oac copy -ovc copy {TEST_VID_PATH} -o ./test_videos/part{i}.mp4"

            # command = f"ffmpeg -i {TEST_VID_PATH} -ss {chunk.start.hours}:{chunk.start.minutes}:{chunk.start.seconds}.{chunk.start.milliseconds} -to {chunk.end.hours}:{chunk.end.minutes}:{chunk.end.seconds}.{chunk.end.milliseconds} -c copy ./test_videos/part{i}.mp4 -y"
            # subprocess.call(command,shell=True)

            # command = f"ffmpeg -i {TEST_AUD_PATH} -ss {chunk.start.hours}:{chunk.start.minutes}:{chunk.start.seconds}.{chunk.start.milliseconds} -t {chunk.end.hours}:{chunk.end.minutes}:{chunk.end.seconds}.{chunk.end.milliseconds}  ./test_audio/part{i}.mp3 -y"
            # subprocess.call(command,shell=True)

            # more accurate trimming than using ffmpeg
            try:
                video_part = videoToSplit.subclip(
                    videoProcessingUtils.convertTimeToSeconds(chunk.start.hours, chunk.start.minutes, chunk.start.seconds, chunk.start.milliseconds),
                    videoProcessingUtils.convertTimeToSeconds(chunk.end.hours, chunk.end.minutes, chunk.end.seconds, chunk.end.milliseconds))
                # audio_part = audio.subclip(get_time_in_seconds(chunk.start.hours,chunk.start.minutes,chunk.start.seconds,chunk.start.milliseconds),get_time_in_seconds(chunk.end.hours,chunk.end.minutes,chunk.end.seconds,chunk.end.milliseconds))

                # time will be in milliseconds since pydub works with milliseconds
                audio_part = audioToSplit[videoProcessingUtils.convertTimeToSeconds(chunk.start.hours, chunk.start.minutes, chunk.start.seconds,
                                                                                    chunk.start.milliseconds) * 1000:videoProcessingUtils.convertTimeToSeconds(chunk.end.hours,
                                                                                                                                                               chunk.end.minutes,
                                                                                                                                                               chunk.end.seconds,
                                                                                                                                                               chunk.end.milliseconds) * 1000]

                videoChunkPath = settings.MEDIA_ROOT + f'/videoSplit/{id}/{i}.mp4'
                audioChunkPath = settings.MEDIA_ROOT + f'/audioSplit/{id}/{i}.mp3'



                video_part.write_videofile(videoChunkPath )
                audio_part.export(audioChunkPath, format="mp3")
                # audio_part.write_audiofile(f'./test_audio/part{i}.mp3')




                #s in front stands for start
                shour,sminute,ssecond,smillisecond = chunk.start
                ehour, eminute, esecond, emillisecond = chunk.end

                # create datetime object

                startTime = datetime.time(chunk.start.hours,chunk.start.minutes,chunk.start.seconds)



                #creating end time datetime object
                endTime = datetime.time(chunk.end.hours,chunk.end.minutes,chunk.end.seconds)


                audio_chunk_url_path = settings.MEDIA_URL + f'audioSplit/{id}/{i}.mp3'
                video_chunk_url_path = settings.MEDIA_URL + f'videoSplit/{id}/{i}.mp4'

                chunkInstance = Chunk(
                    operationId= videoFile,
                    me = i,
                    videoChunkPath=video_chunk_url_path,
                    videoChunkName=f'{i}.mp4',
                    audioChunkPath=audio_chunk_url_path,
                    audioChunkName=f'{i}.mp3',
                    subtitleChunk = chunk.text,
                    startTime= startTime,
                    endTime = endTime,
                )

                chunkInstance.save()

                data = {"start": chunk.start, "end": chunk.end, "text": chunk.text, "video": videoChunkPath,
                        "audio": audioChunkPath}
                # split video here.
                subData.append(data)
                i = i + 1
            except ValueError:
                break
        #fetching data from db.
        video = VideoModel.objects.get(pk=id)
        chunks = video.rel.all()
        serializeChunk = ChunkSerializer(chunks, many=True)

        #building response object
        message = {
            "message": "success",
            "time(sec)": f'Time: {time.time() - start}',
            "path": f"/api/fetchdetails/{id}",
            "downloadUrl":f"/api/download/{id}",
            "chunks": serializeChunk.data,
        }

        return Response(message, status=status.HTTP_200_OK)
        #extract audio and save it in directory as well as database with reference to id.
        # message = {
        #     "message" : "success",
        #     "view details" : f"/api/fetchdetails/{id}"
        # }
        # return Response(message)
        # return redirect(f'fetchdetails/{id}')




@api_view(['POST'])
def reupload_audio_chunk(request,chunk_id):
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

        print("hello!!!")
        print(request.FILES['file'].name)

        #duration of audio chunk in seconds
        length_of_audio_chunk = videoProcessingUtils.getVideoLengthInSeconds(chunk.endTime, chunk.startTime)




        audio_chunk_save_path = settings.BASE_DIR  + chunk.audioChunkPath
        print(audio_chunk_save_path)
        audio_chunk_path = settings.MEDIA_ROOT +f"re-uploads/{chunk_id}.mp3"
        #
        videoProcessingUtils.trimVideoClipAndSave(audio_chunk_path, 0, length_of_audio_chunk, audio_chunk_save_path)
        #
        #
        file = audio_chunk_save_path
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        # playing sound using pygames.


        # update audio chunk of this chunk
        # chunk.audioChunkPath = f"/audioSplit/{chunk.operationId}/{chunk_id}.mp3"
        # chunk.save()



        return redirect(f"/api/fetchdetails/{chunk.operationId}")

@api_view(['GET'])
def download_final(request,operationId):


    bashFiles_path = settings.MEDIA_ROOT + "bashFiles"


    #creating directory to bashFiles with operationId as name
    id_as_dir_name = bashFiles_path + f"/{operationId}/"


    #remove comment after test
    if os.path.exists(id_as_dir_name):
        shutil.rmtree(id_as_dir_name)


    try:
        os.mkdir(id_as_dir_name)
        chunks = Chunk.objects.all().filter(operationId=operationId)


        audi_file_path = f"{bashFiles_path}/{operationId}/{operationId}AUDI.txt"
        vid_file_path = f"{bashFiles_path}/{operationId}/{operationId}VID.txt"



        merged_audio_destination_path = settings.MEDIA_ROOT+f"audioSplit/{operationId}/mergedAUDIO.mp3"
        merged_video_destination_path = settings.MEDIA_ROOT+f"videoSplit/{operationId}/mergedVIDEO.mp4"

        path__to_final_downloadable = settings.MEDIA_ROOT + "downloadable/"

        # check to see if files already exist if exists remove it
        if  os.path.exists(merged_audio_destination_path):
            os.remove(merged_audio_destination_path)

        #removeing the last slash as its causing problem

        # -7 to strip last 7 characters in settings.MEDIA_ROOT to avoid repetition.
        media_path = settings.MEDIA_ROOT[:-7]
        audiFile = open(audi_file_path, 'a')
        vidFile = open(vid_file_path, 'a')
        for chunk in chunks:
            audio_chunk_path = media_path + chunk.audioChunkPath

            video_chunk_path = media_path + chunk.videoChunkPath
            audiFile.write(f"file '{audio_chunk_path}'\n")
            vidFile.write(f"file '{video_chunk_path}'\n")
        audiFile.close()
        vidFile.close()



        # use the above files to combne audios and videos
        command_for_merging_audios = f"ffmpeg -f concat -safe 0 -i {audi_file_path} -c copy {merged_audio_destination_path} -y"
        command_for_merging_videos = f"ffmpeg -f concat -safe 0 -i {vid_file_path} -c copy {merged_video_destination_path} -y"

        subprocess.call(command_for_merging_audios, shell=True)

        subprocess.call(command_for_merging_videos, shell=True)

        if not os.path.exists(merged_audio_destination_path) and not os.path.exists(merged_video_destination_path):
            return Response({
                "message" : "failed to create batch file",
            })


        command_for_merging_audio_video = f"ffmpeg -i {merged_video_destination_path} -i {merged_audio_destination_path} -c copy {path__to_final_downloadable}{operationId}.mp4 -y"
        subprocess.call(command_for_merging_audio_video,shell=True)


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
    except:
        response = Response({
            "message":"Error occured while processing."
        },status=status.HTTP_409_CONFLICT)

    return response