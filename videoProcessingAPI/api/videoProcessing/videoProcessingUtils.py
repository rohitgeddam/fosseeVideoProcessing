from django.conf import settings
from moviepy.editor import *

import subprocess
import pysrt
import os


class SRT:
    def __init__(self,path):
        self.instance = pysrt.open(path)

    def numberOfChunksInSrt(self):
        return len(self.instance)

    def extractSrtData(self):
        return self.instance



class VideoClip:
    def __init__(self,path):
        self.path = path
        self.instance =  VideoFileClip(os.path.join(settings.MEDIA_ROOT,path))

    def extractAudioFromVideoAndSave(self, path, saveAs):
        command = f"ffmpeg -i {self.path} -ab 160k -ac 2 -ar 44100 -vn {path}/{saveAs} -y"
        subprocess.call(command, shell=True)
        return f"{path}/{saveAs}"

    def removeAudioFromVideoAndSave(self, path, saveAs):
        command = f"ffmpeg -i {self.path} -vcodec copy -an {path}/{saveAs} -y"
        subprocess.call(command, shell=True)
        return f"{path}/{saveAs}"



def mergeVideoAndAudioToGetDownloadFile(operationId,videoPath,audioPath,pathToSaveTo):
        print(videoPath)
        print(audioPath)
        command_for_merging_audio_video = f"ffmpeg -i {videoPath} -i {audioPath} -c copy {pathToSaveTo}{operationId}.mp4 -y"
        subprocess.call(command_for_merging_audio_video, shell=True)

def mergeAudiosForDownload(audi_file_path,merged_audio_destination_path):
    print("ERROR HERRE")
    print(audi_file_path)
    print(merged_audio_destination_path)
    command_for_merging_audios = f"ffmpeg -f concat -safe 0 -i {audi_file_path} -c copy {merged_audio_destination_path} -y"
    subprocess.call(command_for_merging_audios, shell=True)

def mergeVideoForDownload(vid_file_path,merged_video_destination_path):
    command_for_merging_videos = f"ffmpeg -f concat -safe 0 -i {vid_file_path} -c copy {merged_video_destination_path} -y"
    subprocess.call(command_for_merging_videos, shell=True)


def trimAudioClipAndSave(path, startingTime, length, save_path):
   
    command = f"ffmpeg -ss {startingTime} -i {path} -t {length} -c copy {save_path} -y"
    subprocess.call(command, shell=True)


def getVideoLengthInSeconds(endTime, startTime):
    total = 0
    total += (endTime.hour - startTime.hour) * 60 * 60
    total += (endTime.minute - startTime.minute) * 60
    total += (endTime.second - startTime.second)

    return total


def convertTimeToSeconds(hours, minutes, seconds, milliseconds):
    """convert time into seconds"""
    h = int(hours) * 3600
    minu = int(minutes) * 60
    sec = int(seconds)
    return h + minu + sec + (milliseconds/1000)