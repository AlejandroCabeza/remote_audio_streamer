# Python Imports
from abc import ABC, abstractmethod
# Third-Party Imports
# Project Imports


class IPlayable(ABC):

    @abstractmethod
    def get_song(self) -> str:
        pass


class IPlayableList(IPlayable, ABC):

    @abstractmethod
    def get_previous_song(self) -> str:
        pass

    @abstractmethod
    def get_next_song(self) -> str:
        pass

    @abstractmethod
    def get_random_song(self) -> str:
        pass
