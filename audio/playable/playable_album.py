# Python Imports
import random
from typing import List, Optional
# Third-Party Imports
# Project Imports
from audio.playable.playable_interfaces import IPlayableList


class PlayableAlbum(IPlayableList):

    def __init__(self, song_path_list: List[str], selected_song_index: Optional[int]):
        self._song_path_list: List[str] = song_path_list
        self._song_path_list_length: int = len(self._song_path_list)
        self._song_index: Optional[int] = selected_song_index

    @property
    def _selected_song_index(self):
        return self._song_index

    @_selected_song_index.setter
    def _selected_song_index(self, value: int):
        self._song_index = value % self._song_path_list_length

    def _update_selected_song_to_previous(self):
        self._selected_song_index -= 1

    def _update_selected_song_to_next(self):
        self._selected_song_index += 1

    def get_song(self) -> str:
        return self._song_path_list[self._selected_song_index]

    def get_previous_song(self) -> str:
        self._update_selected_song_to_previous()
        return self.get_song()

    def get_next_song(self) -> str:
        self._update_selected_song_to_next()
        return self.get_song()

    def get_random_song(self) -> str:
        return random.choice(self._song_path_list)
