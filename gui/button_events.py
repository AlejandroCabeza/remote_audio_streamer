# Python Imports
# Third-Party Imports
from PySide2.QtCore import QModelIndex, QFileInfo
# Project Imports
from audio.engine.loop_modes import LoopModes
from gui.decorators import only_if_audio_engine_defined
from audio.engine.audio_engine_interfaces import IAudioEngine
from gui.utils.audio_engine_utils import play_file_info_directory


@only_if_audio_engine_defined
def on_button_play_pause_toggled(_button, audio_engine: IAudioEngine, is_toggled: bool):
    if is_toggled:
        audio_engine.pause()
    else:
        audio_engine.resume()


@only_if_audio_engine_defined
def on_button_loop_clicked(_button, audio_engine: IAudioEngine):
    loop_mode: LoopModes = audio_engine.loop_toggle()
    _button.setText(f"Loop: {loop_mode.name.capitalize()}")


@only_if_audio_engine_defined
def on_button_volume_up_clicked(_button, audio_engine: IAudioEngine):
    audio_engine.volume_up()


@only_if_audio_engine_defined
def on_button_volume_down_clicked(_button, audio_engine: IAudioEngine):
    audio_engine.volume_down()


@only_if_audio_engine_defined
def on_slider_song_progress_pressed(_slider, audio_engine: IAudioEngine):
    audio_engine.pause()


@only_if_audio_engine_defined
def on_slider_song_progress_released(_slider, audio_engine: IAudioEngine):
    audio_engine.resume()


@only_if_audio_engine_defined
def on_slider_song_progress_value_change(_slider, audio_engine: IAudioEngine, value: int):
    audio_engine.set_song_progress_percentage(value)


@only_if_audio_engine_defined
def on_slider_volume_value_change(_slider, audio_engine: IAudioEngine, value: int):
    audio_engine.volume_percentage = value


@only_if_audio_engine_defined
def on_widget_file_click(_widget, audio_engine: IAudioEngine, model_index: QModelIndex):
    file_info: QFileInfo = model_index.model().fileInfo(model_index)
    if not file_info.isDir():
        play_file_info_directory(audio_engine, file_info)
