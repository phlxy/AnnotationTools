from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QFrame, QPushButton
from PyQt6.QtCore import Qt
from controllers.zoom_controller import ZoomController

class ZoomView(QWidget):
    def __init__(self, parent: QWidget, controller: ZoomController):
        super().__init__()
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)  # Initialize the layout
        self.setLayout(self.layout)       # Set the layout for the widget

        # Zoom Controls
        self.layout.addWidget(self.create_separator())
        
        self.zoom_out_btn = QPushButton("🔍-")
        self.zoom_out_btn.clicked.connect(self.on_zoom_out)
        self.layout.addWidget(self.zoom_out_btn)

        self.zoom_reset_btn = QPushButton("100%")
        self.zoom_reset_btn.clicked.connect(self.on_zoom_reset)
        self.layout.addWidget(self.zoom_reset_btn)

        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_in_btn.clicked.connect(self.on_zoom_in)
        self.layout.addWidget(self.zoom_in_btn)

    def on_zoom_in(self):
        """จัดการการซูมเข้า"""
        scale = min(2.0, self.controller.annotation_controller.scale_factor * 1.2)
        self.controller.annotation_controller.set_scale_factor(scale)
        self.update_zoom_button()

    def on_zoom_out(self):
        """จัดการการซูมออก"""
        scale = max(0.1, self.controller.annotation_controller.scale_factor / 1.2)
        self.controller.annotation_controller.set_scale_factor(scale)
        self.update_zoom_button()

    def on_zoom_reset(self):
        """รีเซ็ตการซูม"""
        self.controller.annotation_controller.set_scale_factor(1.0)
        self.update_zoom_button()

    def update_zoom_button(self):
        """อัพเดทปุ่มซูม"""
        scale = self.controller.annotation_controller.scale_factor
        self.zoom_reset_btn.setText(f"{int(scale * 100)}%")