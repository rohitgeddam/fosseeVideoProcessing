from django.test import SimpleTestCase
from django.urls import reverse,resolve

from api.views import uploadFilesToServer,\
    getVideoDetails,splitVideo,\
    reuploadAudioChunk,processAndGenerateFinalVideo


class TestUrls(SimpleTestCase):

    def test_upload_file_url(self):
        url = reverse("file-upload")

        self.assertEquals(resolve(url).func,uploadFilesToServer)

    def test_get_details_url(self):
        url = reverse("get-details",kwargs={"id":1})

        self.assertEquals(resolve(url).func, getVideoDetails)

    def test_process_url(self):
        url = reverse("process",kwargs={"id":1})

        self.assertEquals(resolve(url).func, splitVideo)

    def test_audio_reupload_url(self):
        url = reverse("audio-reupload", kwargs={"chunk_id": 1})

        self.assertEquals(resolve(url).func, reuploadAudioChunk)

    def test_download_url(self):
        url = reverse("download", kwargs={"operationId": 1})

        self.assertEquals(resolve(url).func, processAndGenerateFinalVideo)