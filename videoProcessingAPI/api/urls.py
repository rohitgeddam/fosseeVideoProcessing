from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('upload/', views.uploadFilesToServer ,name ="file-upload"),
    # path('getdetails/', views.getListOfPreviouslyProcessedVideos),
    # path('getdetails/<int:id>', views.getVideoDetails,name="get-details"),
    path('process/<int:id>',views.splitVideo,name="process"),

    path('reupload/<int:chunk_id>',views.reuploadAudioChunk,name="audio-reupload"),

    path('download/<int:operationId>',views.processAndGenerateFinalVideo),

]
