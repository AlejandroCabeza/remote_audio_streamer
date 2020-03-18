# Python Imports
# Third-Party Imports
from PySide2.QtCore import QFileInfo
# Project Imports
from audio.playable.playable_album import PlayableAlbum
from audio.engine.audio_engine_interfaces import IAudioEngine
from gui.utils.directory_utils import create_file_siblings_path_list_from_file_info


def play_file_info_directory(audio_engine: IAudioEngine, file_info: QFileInfo):
    album = create_file_siblings_path_list_from_file_info(file_info)
    index = album.index(file_info.filePath())
    audio_engine.play(PlayableAlbum(album, index))
