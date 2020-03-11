# Python Imports
from typing import Set
from collections import Callable
# Third-Party Imports
# Project Imports


class ISongVolumeLevelObservable:

    def __init__(self, volume_level_percentage_subscribers: Set[Callable], **kwargs):
        super().__init__(**kwargs)
        self._volume_level_percentage_subscribers: Set[Callable] = (
            volume_level_percentage_subscribers
            if volume_level_percentage_subscribers else
            set()
        )

    def subscribe_to_volume_level_percentage(self, subscriber: Callable):
        self._volume_level_percentage_subscribers.add(subscriber)

    def notify_all_volume_level_percentage_subscribers(self, volume_level: float):
        for subscriber in self._volume_level_percentage_subscribers:
            subscriber(volume_level)


class ISongProgressPercentageObservable:

    def __init__(self, song_progress_percentage_subscribers: Set[Callable], **kwargs):
        super().__init__(**kwargs)
        self._song_progress_percentage_subscribers: Set[Callable] = (
            song_progress_percentage_subscribers
            if song_progress_percentage_subscribers else
            set()
        )

    def subscribe_to_song_progress_percentage(self, subscriber: Callable):
        self._song_progress_percentage_subscribers.add(subscriber)

    def notify_all_song_progress_percentage_subscribers(self, song_progress_percentage: int):
        for subscriber in self._song_progress_percentage_subscribers:
            subscriber(song_progress_percentage)
