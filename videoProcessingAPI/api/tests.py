from django.test import TestCase

from rest_framework import status

import os

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.core import serializers
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile



class FileUploadTests(APITestCase):

    def _create_test_file(self,video_path,srt_path):


        video_file = SimpleUploadedFile(video_path,b"file_content",content_type="video/mp4")
        srt_file = SimpleUploadedFile(srt_path,b"file_content",content_type="text/plain")
        return {
            "video" : video_file,
            "srt" : srt_file
        }

    def test_upload_file(self):
        test_video_path = os.path.join(settings.BASE_DIR,"./test_files/test.mp4")
        test_srt_path = os.path.join(settings.BASE_DIR,"./test_files/test.srt")
        url = reverse("file-upload")
        data = self._create_test_file(test_video_path,test_srt_path)

        client = APIClient()
        response = client.post(url,data,format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class VideoSplit(APITestCase):


    def test_video_split(self):

        client = APIClient()

        operation_id = 1
        url = reverse("process", kwargs={'id':operation_id})
        response= client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


