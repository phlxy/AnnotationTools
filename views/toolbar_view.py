from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QFrame)
from controllers.label_controller import LabelController
from controllers.zoom_controller import ZoomController
from config.config import Config
from .zoom_view import ZoomView
from .label_view import LabelView

class ToolbarView(QWidget):
    def __init__(self):
        super().__init__()
        self.labelController = LabelController()
        self.zoomController = ZoomController()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)  # เพิ่ม margin รอบๆ layout หลัก
        self.layout.setSpacing(10)  # เพิ่มระยะห่างระหว่าง widgets
        self.setup_ui()
    
    def setup_ui(self):
        # Toolbar ชุดแรก
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 10)  # เพิ่ม margin ให้กับ toolbar
        toolbar.setSpacing(10)  # เพิ่ม spacing ระหว่าง widgets ใน toolbar

        self.label_view = LabelView(self, self.labelController)
        toolbar.addWidget(self.label_view)

        # Zoom View
        self.zoom_view = ZoomView(self.zoomController)
        toolbar.addWidget(self.zoom_view)

        self.layout.addLayout(toolbar)  # เพิ่ม toolbar layout เข้าไปใน layout หลัก

