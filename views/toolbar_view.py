from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, 
    QFrame, QFileDialog, QMessageBox
)
from PyQt6.QtCore import pyqtSignal

from controllers.label_controller import LabelController
from controllers.zoom_controller import ZoomController
from controllers.file_controller import FileController
from .zoom_view import ZoomView
from .label_view import LabelView

class ToolbarView(QWidget):
    """Widget แสดงแถบเครื่องมือหลักของแอพพลิเคชัน"""

    def __init__(self):
        super().__init__()
        
        # Initialize controllers
        self.labelController = LabelController()
        self.zoomController = ZoomController()
        self.fileController = FileController()

        # Setup UI
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.setup_ui()
        self._connect_signals()

    def setup_ui(self):
        """สร้างและจัดวาง UI components"""
        # Label View
        self.label_view = LabelView(self, self.labelController)
        self.layout.addWidget(self.label_view)

        # Add separator
        self.layout.addWidget(self._create_separator())

        # File tools
        self.setup_file_tools()

        # Add separator
        self.layout.addWidget(self._create_separator())

        # Zoom View
        self.zoom_view = ZoomView(self.zoomController)
        self.layout.addWidget(self.zoom_view)

        # Add separator
        self.layout.addWidget(self._create_separator())

        # Export tools
        self.setup_export_tools()

        # Add stretch to push everything to the left
        self.layout.addStretch()

    def setup_file_tools(self):
        """สร้าง UI สำหรับจัดการไฟล์"""
        # Load single file button
        self.load_btn = QPushButton("เลือกไฟล์")
        self.load_btn.setFixedWidth(100)
        self.load_btn.clicked.connect(self._on_load_file)
        self.layout.addWidget(self.load_btn)
        
        # Load multiple files button
        self.load_batch_btn = QPushButton("เพิ่มหลายไฟล์")
        self.load_batch_btn.setFixedWidth(100)
        self.load_batch_btn.clicked.connect(self._on_load_batch)
        self.layout.addWidget(self.load_batch_btn)

    def setup_export_tools(self):
        """สร้าง UI สำหรับการ export"""
        # Validate button
        self.validate_btn = QPushButton("ตรวจสอบ")
        self.validate_btn.setFixedWidth(80)
        self.validate_btn.clicked.connect(self._on_validate)
        self.layout.addWidget(self.validate_btn)
        
        # Export button
        self.export_btn = QPushButton("ส่งออก")
        self.export_btn.setFixedWidth(80)
        self.export_btn.clicked.connect(self._on_export)
        self.layout.addWidget(self.export_btn)

    def _create_separator(self) -> QFrame:
        """สร้าง vertical separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator

    def _connect_signals(self):
        """เชื่อมต่อ signals ระหว่าง components"""
        self.fileController.error_occurred.connect(self._handle_error)

    def _handle_error(self, message: str):
        """แสดง error message"""
        QMessageBox.warning(self, "Error", message)

    def _on_load_file(self):
        """จัดการการเลือกไฟล์เดียว"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "เลือกเอกสาร",
            "",
            "Documents (*.pdf *.jpg *.jpeg *.png)"
        )
        
        if file_path:
            self.fileController.load_file(file_path)

    def _on_load_batch(self):
        """จัดการการเลือกหลายไฟล์"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "เลือกหลายไฟล์",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )
        
        for file_path in file_paths:
            self.fileController.load_file(file_path)

    def _on_validate(self):
        """ตรวจสอบ annotations"""
        # TODO: Implement validation
        pass

    def _on_export(self):
        """ส่งออกไฟล์"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์สำหรับบันทึก"
        )
        
        if directory:
            # TODO: Implement export
            pass