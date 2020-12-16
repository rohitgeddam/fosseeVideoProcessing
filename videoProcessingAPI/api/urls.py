from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path("upload/", views.upload_files_to_server, name="file-upload"),
    # path('getdetails/', views.getListOfPreviouslyProcessedVideos),
    path("getdetails/<int:id>", views.get_video_details, name="get-details"),
    path("process/<int:id>", views.split_video, name="process"),
    path("reupload/<int:chunk_id>", views.reupload_audio_chunk, name="audio-reupload"),
    path(
        "download/<int:operationId>",
        views.process_and_generate_final_video,
        name="download",
    ),
]
