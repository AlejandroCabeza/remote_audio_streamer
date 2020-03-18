# Python Imports
# Third-Party Imports
from PySide2.QtCore import QFileInfo, QDir
# Project Imports


def create_file_siblings_path_list_from_file_info(file_info: QFileInfo):
    return [
        sibling_file_info.filePath()
        for sibling_file_info
        in file_info.dir().entryInfoList(filters=QDir.Files)
    ]
