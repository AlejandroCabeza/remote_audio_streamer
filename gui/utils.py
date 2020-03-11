# Python Imports
# Third-Party Imports
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget
# Project Imports


def load_widget_from_ui_file(filepath: str) -> QWidget:
    q_file: QFile = QFile(filepath)
    q_file.open(QFile.ReadOnly)
    widget: QUiLoader = QUiLoader().load(q_file)
    q_file.close()
    return widget
