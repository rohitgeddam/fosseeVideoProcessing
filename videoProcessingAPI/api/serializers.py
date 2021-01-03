from rest_framework import serializers
from api import models


class VideoFileSerializer(serializers.ModelSerializer):
    """Serializer for Video"""

    class Meta:
        model = models.VideoModel
        fields = ("id", "video", "path")


class AudioFileSerializer(serializers.ModelSerializer):
    """Serializer for Audio"""

    class Meta:
        model = models.AudioModel
        fields = ("id", "audio", "path")


class SrtFileSerializer(serializers.ModelSerializer):
    """Serializer for Srt"""

    class Meta:
        model = models.SrtModel
        fields = ("id", "srt", "path")


class ChunkSerializer(serializers.ModelSerializer):
    """Serializer for Chunk"""

    class Meta:
        model = models.Chunk
        fields = "__all__"
