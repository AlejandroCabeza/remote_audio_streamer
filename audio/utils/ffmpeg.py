# Python Imports
from subprocess import Popen
# Third-Party Imports
import ffmpeg
# Project Imports


def get_raw_audio_data_from_audio_file(audio_file_path: str, channels: int, sampling_rate: int) -> bytes:
    audio, _video = ffmpeg.input(
        audio_file_path,
        loglevel="warning"
    ).output(
        "-",
        format="s16le",
        acodec="pcm_s16le",
        ac=channels,
        ar=sampling_rate
    ).run(
        capture_stdout=True
    )
    return audio


def get_raw_audio_data_from_audio_file_process(audio_file_path: str, channels: int, sampling_rate: int) -> Popen:
    return ffmpeg.input(
        audio_file_path,
        loglevel="warning"
    ).output(
        "pipe:",
        format="s16le",
        acodec="pcm_s16le",
        ac=channels,
        ar=sampling_rate
    ).run_async(
        pipe_stdout=True
    )
