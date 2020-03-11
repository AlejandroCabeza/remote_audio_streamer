# Python Imports
from abc import ABC, abstractmethod
# Third-Party Imports
from discord import AudioSource
# Project Imports


class IAudioSource(ABC):

    @abstractmethod
    def read(self) -> bytes:
        pass

    @abstractmethod
    def set_song_progress_percentage(self, song_progress_percentage: int):
        pass

    @abstractmethod
    def reset_audio_source(self):
        pass


class IDiscordAudioSource(IAudioSource, AudioSource, ABC):
    pass
