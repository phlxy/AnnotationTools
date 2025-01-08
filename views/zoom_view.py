# views/zoom_view.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class ZoomView(QWidget):
    def __init__(self, zoom_controller):
        super().__init__()
        self.controller = zoom_controller
        self.controller.add_view(self)
        self.setup_ui()

    def setup_ui(self):
        """ตั้งค่า UI สำหรับการซูม"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # ปุ่มซูมออก
        self.zoom_out_btn = QPushButton("🔍-")
        self.zoom_out_btn.setFixedWidth(50)
        self.zoom_out_btn.clicked.connect(self.controller.zoom_out)
        layout.addWidget(self.zoom_out_btn)

        # แสดงค่าซูม
        self.zoom_label = QPushButton("100%")
        self.zoom_label.setFixedWidth(60)
        self.zoom_label.clicked.connect(self.controller.reset_zoom)
        layout.addWidget(self.zoom_label)

        # ปุ่มซูมเข้า
        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_in_btn.setFixedWidth(50)
        self.zoom_in_btn.clicked.connect(self.controller.zoom_in)
        layout.addWidget(self.zoom_in_btn)

    def update_zoom(self, zoom_percentage):
        """อัพเดทการแสดงค่าซูม"""
        self.zoom_label.setText(f"{zoom_percentage}%")

    def wheelEvent(self, event):
        """จัดการการซูมด้วยเมาส์"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.controller.zoom_in()
            else:
                self.controller.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)