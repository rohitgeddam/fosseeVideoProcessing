from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('upload/', views.uploadFilesToServer),
    path('getdetails/', views.getListOfPreviouslyProcessedVideos),
    path('getdetails/<int:id>', views.getVideoDetails),
    path('process/<int:id>',views.split_video),
    path('reupload/<int:chunk_id>',views.reupload_audio_chunk),
    path('download/<int:operationId>',views.download_final),

]
