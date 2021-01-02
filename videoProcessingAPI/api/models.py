import os

from django.db import models
from django.core.files.storage import FileSystemStorage


class AudioModel(models.Model):
    audio = models.FileField(upload_to="re-uploads/", blank=False)
    path = models.CharField(max_length=500, blank=False, default="~/")

    def __str__(self):
        return str(self.pk)


class VideoModel(models.Model):
    video = models.FileField(upload_to="videos/", blank=False)
    path = models.CharField(max_length=500, blank=False, default="~/")

    def __str__(self):
        return str(self.pk)


class SrtModel(models.Model):
    srt = models.FileField(upload_to="srts/", null=False)
    path = models.CharField(max_length=500, null=False, default="~/")

    def __str__(self):
        return str(self.pk)


class Chunk(models.Model):
    operationId = models.ForeignKey(
        VideoModel,
        default=1,
        verbose_name="operationId",
        on_delete=models.SET_DEFAULT,
        related_name="rel",
    )
    me = models.IntegerField(default=0)
    videoChunkPath = models.CharField(
        max_length=200, blank=False, null=False, default="~/"
    )
    videoChunkName = models.CharField(max_length=100, blank=False, default="1.mp4")
    videoChunkLocalPath = models.CharField(max_length=100, blank=False, default="1.mp4")
    audioChunkLocalPath = models.CharField(max_length=100, blank=False, default="1.mp3")
    audioChunkPath = models.CharField(
        max_length=200, blank=False, null=False, default="~/"
    )
    audioChunkName = models.CharField(
        max_length=200, blank=False, null=False, default="1.mp3"
    )
    subtitleChunk = models.CharField(
        max_length=500, blank=True, null=False, default=" "
    )
    startTime = models.TimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False
    )
    endTime = models.TimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False
    )


class FusedResult(models.Model):
    operationId = models.ForeignKey(
        VideoModel, default=1, verbose_name="operationId", on_delete=models.SET_DEFAULT
    )
    videoPath = models.CharField(max_length=200, blank=False, null=False, default="~/")
    videoName = models.CharField(
        max_length=100, blank=False, null=False, default="a.mp4"
    )
    videoUrl = models.CharField(
        max_length=500, blank=False, null=False, default="/media/downloadable/"
    )

    def __str__(self):
        return self.videoName
