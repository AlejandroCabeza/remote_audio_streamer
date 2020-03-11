# Python Imports
from typing import Callable, Set
# Third-Party Imports
from discord.opus import Encoder as OpusEncoder
# Project Imports
from utils.math import clamp
from audio.utils.volume import apply_volume_to_bytes
from audio.source.audio_source_interfaces import IDiscordAudioSource
from audio.buffer.audio_buffer import IAudioBuffer, SynchronousAudioBuffer


class DiscordAudioSource(IDiscordAudioSource):

    def __init__(self, audio_file_path: str, song_percentage_subscribers: Set[Callable] = None, volume: float = 1.0):
        self.volume: float = volume
        self.audio_buffer: IAudioBuffer = SynchronousAudioBuffer(
            audio_file_path,
            OpusEncoder.CHANNELS,
            OpusEncoder.SAMPLING_RATE,
            OpusEncoder.FRAME_SIZE
        )
        self._song_progress_percentage: int = 0
        self._song_percentage_subscribers: Set[Callable] = song_percentage_subscribers

    def read(self) -> bytes:
        audio_bytes: bytes = self._read_audio_bytes_and_apply_volume()
        self._update_song_progress_percentage_if_needed()
        return audio_bytes

    def _read_audio_bytes_and_apply_volume(self):
        audio_bytes: bytes = self.audio_buffer.read()
        return apply_volume_to_bytes(audio_bytes, self.volume)

    def _update_song_progress_percentage_if_needed(self):
        audio_source_position_as_percentage: int = int(self.audio_buffer.get_pointer_position_as_percentage())
        if self._song_progress_percentage != audio_source_position_as_percentage:
            # Slowing down
            self._song_progress_percentage = audio_source_position_as_percentage
            # self.audio_buffer.set_pointer_position_from_percentage(self._song_progress_percentage)
            self._notify_all_song_progress_subscribers(audio_source_position_as_percentage)

    def reset_audio_source(self):
        self.set_song_progress_percentage(0)

    def set_song_progress_percentage(self, song_progress_percentage: int):
        self._song_progress_percentage = int(clamp(song_progress_percentage, 0, 100))
        self.audio_buffer.set_pointer_position_from_percentage(self._song_progress_percentage)
        self._notify_all_song_progress_subscribers(song_progress_percentage)

    def _notify_all_song_progress_subscribers(self, song_progress_percentage: int):
        for subscriber in self._song_percentage_subscribers:
            subscriber(song_progress_percentage)
