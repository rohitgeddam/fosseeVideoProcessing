from django.test import SimpleTestCase
from django.urls import reverse, resolve

from api.views import (
    upload_files_to_server,
    get_video_details,
    split_video,
    reupload_audio_chunk,
    process_and_generate_final_video,
)


class TestUrls(SimpleTestCase):
    def test_upload_file_url(self):
        url = reverse("file-upload")

        self.assertEquals(resolve(url).func, upload_files_to_server)

    def test_get_details_url(self):
        url = reverse("get-details", kwargs={"id": 1})

        self.assertEquals(resolve(url).func, get_video_details)

    def test_process_url(self):
        url = reverse("process", kwargs={"id": 1})

        self.assertEquals(resolve(url).func, split_video)

    def test_audio_reupload_url(self):
        url = reverse("audio-reupload", kwargs={"chunk_id": 1})

        self.assertEquals(resolve(url).func, reupload_audio_chunk)

    def test_download_url(self):
        url = reverse("download", kwargs={"operationId": 1})

        self.assertEquals(resolve(url).func, process_and_generate_final_video)