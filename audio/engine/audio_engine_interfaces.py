# Python Imports
from typing import Set, Callable
from abc import ABC, abstractmethod
# Third-Party Imports
# Project Imports
from audio.playable.playable_interfaces import IPlayableList
from audio.utils.observer import ISongProgressPercentageObservable, ISongVolumeLevelObservable


class IAudioEngine(ABC):

    @property
    @abstractmethod
    def volume_percentage(self) -> float:
        pass

    @volume_percentage.setter
    @abstractmethod
    def volume_percentage(self, value: float):
        pass

    @abstractmethod
    def play(self, playable_list: IPlayableList):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def previous(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def loop_toggle(self):
        pass

    @abstractmethod
    def set_song_progress_percentage(self, percentage_value: int):
        pass

    @abstractmethod
    def set_volume_level(self, percentage_value: int):
        pass

    @abstractmethod
    def volume_up(self):
        pass

    @abstractmethod
    def volume_down(self):
        pass


class IObservableAudioEngine(ISongVolumeLevelObservable, ISongProgressPercentageObservable, IAudioEngine, ABC):

    def __init__(self, volume_level_percentage_subscribers: Set[Callable] = None,
                 song_progress_percentage_subscribers: Set[Callable] = None):
        super().__init__(volume_level_percentage_subscribers=volume_level_percentage_subscribers,
                         song_progress_percentage_subscribers=song_progress_percentage_subscribers)
