# Python Imports
# Third-Party Imports
from PySide2.QtWidgets import QPushButton
# Project Imports


class QToggleButton(QPushButton):

    def __init__(self, text_off: str, text_on: str, parent_instance: QPushButton):
        super().__init__(parent_instance.icon(), parent_instance.text(), parent_instance.parent())
        self.setCheckable(self._is_toggleable)
        self.setSizePolicy(parent_instance.sizePolicy())
        self.state: bool = parent_instance.isChecked()
        self.text_on: str = text_on
        self.text_off: str = text_off
        self._update_text_for_button_state()
        self.toggled.connect(self._toggle_button)

    @property
    def _is_toggleable(self) -> bool:
        return True

    def _update_text_for_button_state(self):
        self.setText(self._get_text_for_state())

    def _get_text_for_state(self):
        return self.text_on if self.state else self.text_off

    def _toggle_button(self):
        self.state = not self.state
        self._update_text_for_button_state()
