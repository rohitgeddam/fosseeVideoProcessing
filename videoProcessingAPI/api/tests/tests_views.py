from django.test import TestCase

from rest_framework import status

import os

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.urls import reverse

from django.conf import settings


from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel


class TestViews(APITestCase):
    def setUp(self):

        self.client = APIClient()
        self.video_path = os.path.join(settings.BASE_DIR, "test_files/test.mp4")
        self.srt_path = os.path.join(settings.BASE_DIR, "test_files/test.srt")
        self.reupload_audio_path = os.path.join(
            settings.BASE_DIR, "api/test_files/reupload_test.mp3"
        )

        self.video_file = SimpleUploadedFile(
            self.video_path, b"file_content", content_type="video/mp4"
        )
        self.srt_file = SimpleUploadedFile(
            self.srt_path, b"file_content", content_type="text/plain"
        )
        self.reupload_audio_chunk = SimpleUploadedFile(
            self.reupload_audio_path, b"file_content", content_type="audio/mp3"
        )

        VideoModel.objects.create(video=self.video_file, path=self.video_path)

        SrtModel.objects.create(
            srt=self.srt_file,
            path=self.srt_path,
        )

        AudioModel.objects.create(
            audio=self.reupload_audio_chunk,
            path=self.reupload_audio_path,
        )

    # def _create_upload_test_file(self,video_path,srt_path):
    #
    #
    #     video_file = SimpleUploadedFile(video_path,b"file_content",content_type="video/mp4")
    #     srt_file = SimpleUploadedFile(srt_path,b"file_content",content_type="text/plain")
    #
    #
    #     return {
    #         "video" : video_file,
    #         "srt" : srt_file
    #     }

    # def _create_reupload_test_file(self, audio_path):
    #
    #
    #     audio_chunk = SimpleUploadedFile(audio_path,b"file_content",content_type="audio/mp3")
    #
    #     return {
    #         "file" : audio_chunk,
    #     }

    def test_upload_file(self):

        url = reverse("file-upload")

        data = {
            "video": self.video_file,
            "srt": self.srt_file,
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_video_split(self):

        operation_id = VideoModel.objects.all().first().pk

        url = reverse("process", kwargs={"id": operation_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #

    def test_get_details(self):

        operation_id = VideoModel.objects.all().first().pk

        url = reverse("get-details", kwargs={"id": operation_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_download(self):
        operation_id = VideoModel.objects.all().first().pk
        url = reverse("download", kwargs={"operationId": operation_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
