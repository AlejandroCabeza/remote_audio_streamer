# Python Imports
import asyncio
from pathlib import Path
from typing import Optional
from functools import partial
# Third-Party Imports
from PySide2.QtCore import QModelIndex, QSize
from PySide2.QtWidgets import QApplication, QPushButton, QSlider, QFileSystemModel, QTreeView, QWidget
from qtmodern.windows import ModernWindow
import qtmodern.styles
# Project Imports
from audio.engine.audio_engine_factory import AudioEngineFactory
from audio.engine.audio_engine_interfaces import IObservableAudioEngine
from gui.button_events import (
    on_widget_file_click,
    on_button_play_pause_toggled,
    on_button_loop_clicked,
    on_button_volume_up_clicked,
    on_button_volume_down_clicked,
    on_slider_song_progress_pressed,
    on_slider_song_progress_released,
    on_slider_song_progress_value_change,
    on_slider_volume_value_change
)
from gui.utils import load_widget_from_ui_file
from gui.widgets.qclickableslider import QClickableSlider
from gui.widgets.qtogglebutton import QToggleButton


class GuiApplication(QApplication):

    def __init__(self, event_loop, root_path_music_library: Path, audio_engine_factory: AudioEngineFactory):
        super().__init__()
        self.event_loop = event_loop
        self.root_path_music_library: str = str(root_path_music_library.absolute())

        # Initialise Audio Engine
        self.audio_engine_factory: AudioEngineFactory = audio_engine_factory
        self.audio_engine: Optional[IObservableAudioEngine] = None
        self._initialise_audio_engine()

        # Initialise UI
        self.widget = load_widget_from_ui_file("resources/qt_gui_markup.ui")
        qtmodern.styles.dark(self)
        self.modern_window = ModernWindow(self.widget)
        self.modern_window.showNormal()
        size = QSize(self.modern_window.size())
        size.setHeight(size.height()+35)
        self.modern_window.setFixedSize(size)

        self.slider_song_progress: Optional[QSlider] = None
        self.slider_volume: Optional[QSlider] = None
        self._initialise_gui()

    def _initialise_audio_engine(self):
        asyncio.run_coroutine_threadsafe(self._set_audio_engine(), self.event_loop)

    async def _set_audio_engine(self):
        self.audio_engine = await self.audio_engine_factory.create_observable_audio_engine()
        self.audio_engine.subscribe_to_song_progress_percentage(self._update_song_progress_percentage)
        self.audio_engine.subscribe_to_volume_level_percentage(self._update_volume_slider_percentage_value)
        self._update_volume_slider_percentage_value(self.audio_engine.volume_percentage)

    def _update_song_progress_percentage(self, percentage: int):
        self.slider_song_progress.setValue(percentage)

    def _update_volume_slider_percentage_value(self, value: int):
        self.slider_volume.setValue(value)

    def _initialise_gui(self):
        self._replace_required_gui_elements()
        self._initialise_gui_file_system_view()
        self._initialise_gui_bar_control()
        self.modern_window.show()

    def _replace_required_gui_elements(self):
        self._replace_song_progress_slider()
        self._replace_play_pause_button()
        self._replace_volume_slider()

    def _replace_song_progress_slider(self):
        slider_song_progress: QSlider = QClickableSlider(
            self.widget.widget_audio_player__bar_control__bar_slider__slider_song_progress
        )
        self.widget.widget_audio_player__bar_control__bar_slider.replaceWidget(
            self.widget.widget_audio_player__bar_control__bar_slider__slider_song_progress,
            slider_song_progress
        )
        self.widget.widget_audio_player__bar_control__bar_slider__slider_song_progress.close()
        self.widget.widget_audio_player__bar_control__bar_slider__slider_song_progress = slider_song_progress
        self.slider_song_progress = slider_song_progress

    def _replace_play_pause_button(self):
        button_toggle_play_pause: QPushButton = QToggleButton(
            "Play",
            "Pause",
            self.widget.widget_audio_player__bar_control__bar_buttons__button_play_pause
        )
        self.widget.widget_audio_player__bar_control__bar_buttons.replaceWidget(
            self.widget.widget_audio_player__bar_control__bar_buttons__button_play_pause,
            button_toggle_play_pause
        )
        self.widget.widget_audio_player__bar_control__bar_buttons__button_play_pause.close()
        self.widget.widget_audio_player__bar_control__bar_buttons__button_play_pause = button_toggle_play_pause

    def _replace_volume_slider(self):
        volume_slider: QSlider = QClickableSlider(
            self.widget.widget_audio_player__bar_control__bar_buttons__slider_volume
        )
        self.widget.widget_audio_player__bar_control__bar_buttons.replaceWidget(
            self.widget.widget_audio_player__bar_control__bar_buttons__slider_volume,
            volume_slider
        )
        self.widget.widget_audio_player__bar_control__bar_buttons__slider_volume.close()
        self.widget.widget_audio_player__bar_control__bar_buttons__slider_volume = volume_slider
        self.slider_volume = volume_slider

    def _initialise_gui_file_system_view(self):
        dir_model = QFileSystemModel()
        dir_model.setRootPath(self.root_path_music_library)
        file_view: QTreeView = self.widget.widget_audio_player__file_view
        file_view.setModel(dir_model)
        file_view.setRootIndex(dir_model.index(self.root_path_music_library))
        file_view.doubleClicked.connect(
            partial(self._on_file_click, file_view)
        )

    def _initialise_gui_bar_control(self):
        self._initialise_gui_button_play_pause()
        self._initialise_gui_button_loop()
        self._initialise_gui_button_volume_up()
        self._initialise_gui_button_volume_down()
        self._initialise_gui_slider_song_progress()
        self._initialise_gui_slider_volume()

    def _initialise_gui_button_play_pause(self):
        button_play_pause: QPushButton = self.widget.widget_audio_player__bar_control__bar_buttons__button_play_pause
        button_play_pause.toggled.connect(
            partial(self._on_button_play_pause_toggled, button_play_pause)
        )

    def _initialise_gui_button_loop(self):
        button_loop: QPushButton = self.widget.widget_audio_player__bar_control__bar_buttons__button_loop
        button_loop.clicked.connect(
            partial(self._on_button_loop_clicked, button_loop)
        )

    def _initialise_gui_button_volume_up(self):
        button_volume_up: QPushButton = self.widget.widget_audio_player__bar_control__bar_buttons__button_volume_up
        button_volume_up.clicked.connect(
            partial(self._on_button_volume_up_clicked, button_volume_up)
        )

    def _initialise_gui_button_volume_down(self):
        button_volume_down: QPushButton = self.widget.widget_audio_player__bar_control__bar_buttons__button_volume_down
        button_volume_down.clicked.connect(
            partial(self._on_button_volume_down_clicked, button_volume_down)
        )

    def _initialise_gui_slider_song_progress(self):
        slider_song_progress: QSlider = self.widget.widget_audio_player__bar_control__bar_slider__slider_song_progress
        slider_song_progress.sliderPressed.connect(
            partial(self._on_slider_song_progress_pressed, slider_song_progress)
        )
        slider_song_progress.sliderReleased.connect(
            partial(self._on_slider_song_progress_released, slider_song_progress)
        )
        slider_song_progress.sliderClicked.connect(
            partial(self._on_slider_song_progress_value_change, slider_song_progress)
        )

    def _initialise_gui_slider_volume(self):
        slider_volume: QSlider = self.widget.widget_audio_player__bar_control__bar_buttons__slider_volume
        slider_volume.sliderClicked.connect(
            partial(self._on_slider_volume_value_change, slider_volume)
        )

    def _on_file_click(self, widget: QWidget, model_index: QModelIndex):
        on_widget_file_click(widget, self.audio_engine, model_index)

    def _on_button_play_pause_toggled(self, button: QPushButton, is_toggled: bool):
        on_button_play_pause_toggled(button, self.audio_engine, is_toggled)

    def _on_button_loop_clicked(self, button: QPushButton):
        on_button_loop_clicked(button, self.audio_engine)

    def _on_button_volume_up_clicked(self, button: QPushButton):
        on_button_volume_up_clicked(button, self.audio_engine)

    def _on_button_volume_down_clicked(self, button: QPushButton):
        on_button_volume_down_clicked(button, self.audio_engine)

    def _on_slider_song_progress_pressed(self, slider: QSlider):
        on_slider_song_progress_pressed(slider, self.audio_engine)

    def _on_slider_song_progress_released(self, slider: QSlider):
        on_slider_song_progress_released(slider, self.audio_engine)

    def _on_slider_song_progress_value_change(self, slider: QSlider, new_slider_value: int):
        on_slider_song_progress_value_change(slider, self.audio_engine, new_slider_value)

    def _on_slider_volume_value_change(self, slider: QSlider, new_slider_value: int):
        on_slider_volume_value_change(slider, self.audio_engine, new_slider_value)
