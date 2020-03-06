from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('upload/', views.uploadFilesToServer),
    path('getdetails/', views.getListOfPreviouslyProcessedVideos),
    path('getdetails/<int:id>', views.getVideoDetails),
    path('process/<int:id>',views.splitVideo),
    path('reupload/<int:chunk_id>',views.reuploadAudioChunk),
    path('download/<int:operationId>',views.processAndGenerateFinalVideo),

]
