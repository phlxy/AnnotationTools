from typing import List
from models.zoom_model import ZoomModel
from PyQt6.QtCore import pyqtSignal, QObject

class ZoomController(QObject):
    label_changed = pyqtSignal(str)
    document_type_changed = pyqtSignal(str)