# Python Imports
from abc import ABC, abstractmethod
# Third-Party Imports
# Project Imports


class IAudioBuffer(ABC):

    @abstractmethod
    def read(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def get_pointer_position_as_percentage(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def set_pointer_position_from_percentage(self, percentage: float):
        raise NotImplementedError
