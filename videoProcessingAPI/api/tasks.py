import time
from celery import shared_task
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from api import videoProcessingUtils
from api import misc
from api.models import VideoModel, SrtModel, Chunk, FusedResult, AudioModel
from api.serializers import VideoFileSerializer, SrtFileSerializer, ChunkSerializer

# @shared_task
# def name(*args):
#     pass


@shared_task(bind=True)
def split_video_celery(self, id):
    start = time.time()

    videoFile = VideoModel.objects.get(id=id)
    videoInstance = videoProcessingUtils.VideoClip(videoFile.path)

    pathToOnlyAudioDir, pathToOnlyVideoDir = misc.create_audio_video_dirs()
    # VideoFileClip from moviepy.editor
    onlyAudioPath, onlyVideoPath = misc.extract_video_audio_seperately_save(
        id, videoInstance, pathToOnlyAudioDir, pathToOnlyVideoDir
    )
    videoToBeSplittedIntoChunks = VideoFileClip(onlyVideoPath)
    audioToBeSplittedIntoChunks = AudioSegment.from_mp3(onlyAudioPath)

    misc.create_dirs_for_splits(id)

    srtFile = SrtModel.objects.get(id=id)
    srtInstance = videoProcessingUtils.SRT(srtFile.path)
    srtData = srtInstance.extractSrtData()

    misc.split_by_chunk(
        id,
        srtData,
        videoToBeSplittedIntoChunks,
        audioToBeSplittedIntoChunks,
        videoFile,
    )
    # fetching data from db.
    videoInstance = VideoModel.objects.get(pk=id)
    chunks = videoInstance.rel.all()
    serializeChunk = misc.serializeObject(ChunkSerializer, chunks, many=True)

    misc.clean_up_dirs(srtFile.path, videoFile.path)
    # building response object
    message = {
        "message": "success",
        "time(sec)": f"Time: {time.time() - start}",
        "path": f"/api/getdetails/{id}",
        "downloadUrl": f"/api/download/{id}",
        "chunks": serializeChunk.data,
    }

    return message
