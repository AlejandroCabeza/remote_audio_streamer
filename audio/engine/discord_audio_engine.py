# Python Imports
from typing import Optional
# Third-Party Imports
from discord import VoiceClient
# Project Imports
from audio.engine.audio_engine_interfaces import IObservableAudioEngine
from audio.engine.volume_options import (
    DEFAULT_VOLUME_NORMALISED,
    MIN_VOLUME_NORMALISED,
    MAX_VOLUME_NORMALISED,
    DEFAULT_VOLUME_INCREMENT_NORMALISED
)
from audio.engine.loop_modes import LoopModes
from audio.source.audio_source_interfaces import IDiscordAudioSource
from audio.source.audio_source_factory import create_discord_audio_source_for_song
from utils.math import clamp, get_percentage_value_from_normalised, get_normalised_value_from_percentage


class DiscordAudioEngine(IObservableAudioEngine):

    def __init__(self, audio_client):
        super().__init__()
        self._audio_client: VoiceClient = audio_client
        self._loop_state: LoopModes = LoopModes.NOT
        self._current_audio_source: Optional[IDiscordAudioSource] = None
        self._volume_normalised: float = DEFAULT_VOLUME_NORMALISED

    @property
    def _audio_source(self) -> IDiscordAudioSource:
        return self._audio_client.source

    def _set_source_volume(self, normalised_volume: float):
        try:
            self._audio_source.volume = normalised_volume
        except AttributeError:
            pass

    def _set_source_song_progress_percentage(self, new_song_progress_percentage: float):
        try:
            self._audio_source.set_song_progress_percentage(int(new_song_progress_percentage))
        except AttributeError:
            pass

    @property
    def volume_percentage(self) -> float:
        return get_percentage_value_from_normalised(self.volume_normalised)

    @volume_percentage.setter
    def volume_percentage(self, value: float):
        self.volume_normalised = get_normalised_value_from_percentage(value)

    @property
    def volume_normalised(self) -> float:
        return self._volume_normalised

    @volume_normalised.setter
    def volume_normalised(self, value: float):
        self._volume_normalised = clamp(value, MIN_VOLUME_NORMALISED, MAX_VOLUME_NORMALISED)
        self._set_source_volume(self._volume_normalised)
        self.notify_all_volume_level_percentage_subscribers(self.volume_percentage)

    def play(self, path: str):
        self.stop()
        self._set_current_audio_source(path)
        self._play_current_audio_source()

    def _set_current_audio_source(self, audio_source_filepath: str):
        self._current_audio_source: IDiscordAudioSource = create_discord_audio_source_for_song(
            audio_source_filepath,
            {self._on_song_progress_percentage_update},
            self._volume_normalised
        )

    def _play_current_audio_source(self):
        self._play_audio_source(self._current_audio_source)

    def _play_audio_source(self, audio_source: IDiscordAudioSource):
        audio_source.reset_audio_source()
        self._audio_client.play(audio_source, after=self._on_song_end_callback)

    def stop(self):
        self._audio_client.stop()
        self._current_audio_source = None

    def resume(self):
        self._audio_client.resume()

    def pause(self):
        self._audio_client.pause()

    def loop_toggle(self):
        self._loop_state = self._loop_state.get_next_key()
        return self._loop_state

    def set_song_progress_percentage(self, song_progress_percentage: int):
        self._set_source_song_progress_percentage(song_progress_percentage)

    def set_volume_level(self, percentage_value: int):
        self.volume_percentage = percentage_value

    def volume_up(self):
        self.volume_normalised += DEFAULT_VOLUME_INCREMENT_NORMALISED

    def volume_down(self):
        self.volume_normalised -= DEFAULT_VOLUME_INCREMENT_NORMALISED

    def _on_song_progress_percentage_update(self, song_progress_percentage: int):
        self.notify_all_song_progress_percentage_subscribers(song_progress_percentage)

    def _on_song_end_callback(self, _error):
        if self._loop_state is LoopModes.ONE:
            self._play_current_audio_source()
