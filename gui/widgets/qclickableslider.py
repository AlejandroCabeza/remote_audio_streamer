# Python Imports
# Third-Party Imports
from PySide2.QtCore import Signal
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QSlider
from PySide2.QtCore import Qt
# Project Imports


class QClickableSlider(QSlider):

    sliderClicked: Signal = Signal(int)

    def __new__(cls, parent_instance: QSlider) -> "QClickableSlider":
        if parent_instance.orientation() == Qt.Horizontal:
            return super().__new__(QHorizontalClickableSlider)
        elif parent_instance.orientation() == Qt.Vertical:
            return super().__new__(QVerticalClickableSlider)
        else:
            return super().__new__(cls)

    def __init__(self, parent_instance: QSlider):
        super().__init__(parent_instance.orientation(), parent_instance.parent())
        self.setSizePolicy(parent_instance.sizePolicy())
        self.setTracking(self._track_value_change_when_dragging)
        self.is_dragging: bool = False

    @property
    def _track_value_change_when_dragging(self):
        return False

    def _toggle_dragging(self):
        self.is_dragging = not self.is_dragging

    def _get_mouse_position_in_slider_as_percentage(self, event) -> float:
        return self.minimum() + ((self.maximum()-self.minimum()) * event.localPos().x()) / self.width()

    def _emit_slider_click(self, mouse_event: QMouseEvent):
        mouse_position = int(self._get_mouse_position_in_slider_as_percentage(mouse_event))
        self.setValue(mouse_position)
        self.sliderClicked.emit(mouse_position)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if self.is_dragging:
            self._emit_slider_click(event)
            self._toggle_dragging()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if not self.isSliderDown():
            self._emit_slider_click(event)
        else:
            self._toggle_dragging()


class QHorizontalClickableSlider(QClickableSlider):
    pass


class QVerticalClickableSlider(QClickableSlider):

    def _get_mouse_position_in_slider_as_percentage(self, event) -> float:
        return self.maximum() - ((self.maximum()-self.minimum()) * event.localPos().y()) / self.height()
