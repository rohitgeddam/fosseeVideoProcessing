# python core modules
import time, datetime, json, os

# 3rd party libraries
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

# django imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse

# imports for video manipulation
from api import videoProcessingUtils, misc
from api.models import VideoModel, Chunk, AudioModel
from api.serializers import ChunkSerializer

from .tasks import split_video_celery, process_and_generate_final_video_celery
from celery.result import AsyncResult


def get_progress(request, task_id):
    """Get Celery Task Status"""

    result = AsyncResult(task_id)

    response_data = {
        "state": result.state,
        "details": result.info,
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@api_view(["POST"])
def upload_files_to_server(request):
    """Upload files to server"""

    if request.method == "POST":
        serializeVideo, serializeSrt, err_message = misc.handleUploadedFilesAndSave(
            request
        )
        if not err_message:
            payload = {
                "operationId": serializeVideo.data["id"],
                "message": "files uploaded successfully",
                "operation_url": f"/api/process/{serializeVideo.data['id']}",
            }
            return Response(payload, status=status.HTTP_201_CREATED)
        else:
            payload = {"message": err_message}
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_video_details(request, id):
    """Get details of video"""

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
    """Split video into chunks"""

    if request.method == "GET":
        task = split_video_celery.delay(id)
        message = {
            "task_id": task.task_id,
        }
        return Response(message, status=status.HTTP_200_OK)


@api_view(["POST"])
def reupload_audio_chunk(request, chunk_id):
    """Reupload audio chunk"""

    if request.method == "POST":
        # upload reuploaded audio chunk and resize it.
        try:
            chunk = Chunk.objects.get(pk=chunk_id)
        except Exception:
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
    """Get the final downloadable video file"""

    task = process_and_generate_final_video_celery.delay(operationId)
    message = {
        "task_id": task.task_id,
    }
    return Response(message, status=status.HTTP_200_OK)
