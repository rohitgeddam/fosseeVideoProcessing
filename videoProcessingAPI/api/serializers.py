from rest_framework import serializers
from api import models

class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoModel
        fields = ('id','video','path')

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AudioModel
        fields = ('id','audio','path')


class SrtFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SrtModel
        fields =('id','srt','path')


class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chunk
        fields = '__all__'