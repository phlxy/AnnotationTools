from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

class ZoomView(QWidget):
    """Widget สำหรับควบคุมการ zoom"""
    
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """สร้าง UI components"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Zoom Out Button
        self.zoom_out_btn = QPushButton("🔍-")
        self.zoom_out_btn.setFixedWidth(40)
        layout.addWidget(self.zoom_out_btn)
        
        # Zoom Label
        self.zoom_label = QLabel("100%")
        self.zoom_label.setFixedWidth(60)
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.zoom_label)
        
        # Zoom In Button
        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_in_btn.setFixedWidth(40)
        layout.addWidget(self.zoom_in_btn)
        
        # Reset Button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedWidth(50)
        layout.addWidget(self.reset_btn)
        
        self.setLayout(layout)
        
    def _connect_signals(self):
        """เชื่อมต่อ signals กับ controller"""
        # Button signals
        self.zoom_out_btn.clicked.connect(self._controller.zoom_out)
        self.zoom_in_btn.clicked.connect(self._controller.zoom_in)
        self.reset_btn.clicked.connect(self._controller.reset_zoom)
        
        # Controller signals
        self._controller.zoom_status_updated.connect(self._update_ui)
    
    def _update_ui(self, status: dict):
        """อัพเดต UI ตามสถานะ zoom"""
        self.zoom_out_btn.setEnabled(status['can_zoom_out'])
        self.zoom_in_btn.setEnabled(status['can_zoom_in'])
        self.zoom_label.setText(f"{status['percent']}%")
    
    def wheelEvent(self, event):
        """จัดการ mouse wheel events"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self._controller.handle_wheel_event(
                event.angleDelta().y(),
                True
            )
            event.accept()
        else:
            super().wheelEvent(event)