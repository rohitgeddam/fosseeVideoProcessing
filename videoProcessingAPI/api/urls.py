from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path("process/<int:id>", views.split_video, name="process"),
    path("upload/", views.upload_files_to_server, name="file-upload"),
    path("status/<str:task_id>", views.get_progress, name="task-status"),
    path("getdetails/<int:id>", views.get_video_details, name="get-details"),
    path("reupload/<int:chunk_id>", views.reupload_audio_chunk, name="audio-reupload"),
    path(
        "generate/<int:operationId>",
        views.process_and_generate_final_video,
        name="generate",
    ),
]
