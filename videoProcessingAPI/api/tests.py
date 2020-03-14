from django.test import TestCase

from rest_framework import status

import os

from rest_framework.test import APITestCase
from rest_framework.test import APIClient,RequestsClient
from django.core import serializers
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import VideoModel ,SrtModel ,Chunk,FusedResult,AudioModel

class TestViews(APITestCase):

    def _create_upload_test_file(self,video_path,srt_path):


        video_file = SimpleUploadedFile(video_path,b"file_content",content_type="video/mp4")
        srt_file = SimpleUploadedFile(srt_path,b"file_content",content_type="text/plain")
        return {
            "video" : video_file,
            "srt" : srt_file
        }


    def _create_reupload_test_file(self, audio_path):


        audio_chunk = SimpleUploadedFile(audio_path,b"file_content",content_type="audio/mp3")

        return {
            "file" : audio_chunk,
        }

    def test_upload_file(self):
        test_video_path = os.path.join(settings.BASE_DIR,"./test_files/test.mp4")
        test_srt_path = os.path.join(settings.BASE_DIR,"./test_files/test.srt")
        url = reverse("file-upload")
        data = self._create_upload_test_file(test_video_path, test_srt_path)

        client = APIClient()
        response = client.post(url,data,format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def test_video_split(self):

        client = APIClient()

        operation_id = 1
        url = reverse("process", kwargs={'id':operation_id})
        response= client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # chunk = Chunk.objects.all()
        # print(chunk)

#


    def test_audio_chunk_reupload(self):
        test_audio_path = os.path.join(settings.BASE_DIR,"./test_files/reupload_test.mp3")
        data = self._create_reupload_test_file(test_audio_path)

        audio_chunk_id = 1
        url = reverse("audio-reupload", kwargs={'chunk_id':audio_chunk_id})
        # client = RequestsClient()
        client = APIClient()
        # response = client.post('http://testserver/api/reupload/1',data,format="multipart")
        response = client.post(url,data,format="multipart")
        self.assertEqual(response.status_code,status.HTTP_200_OK)



