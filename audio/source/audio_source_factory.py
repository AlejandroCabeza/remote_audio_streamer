# Python Imports
from typing import Callable, Set
# Third-Party Imports
# Project Imports
from audio.source.audio_source_interfaces import IDiscordAudioSource
from audio.source.discord_audio_source import DiscordAudioSource


def create_discord_audio_source_for_song(song_path: str, song_progress_percentage_subscribers: Set[Callable] = None,
                                         volume: float = 1.0) -> IDiscordAudioSource:
    return DiscordAudioSource(song_path, song_progress_percentage_subscribers, volume)
