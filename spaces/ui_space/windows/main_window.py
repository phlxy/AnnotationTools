# spaces/ui_space/windows/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, space_manager):
        super().__init__()
        self.space_manager = space_manager
        self.setWindowTitle("เครื่องมือ Annotation เอกสาร")
        self.setGeometry(100, 100, 1200, 800)
        
        # สร้าง UI เริ่มต้น
        self.setup_ui()
        
        # ลงทะเบียน events
        self.setup_event_handlers()

    def setup_ui(self):
        # สร้าง widget หลัก
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Toolbar
        toolbar = QHBoxLayout()
        
        # Document Type Selector
        self.doc_type_label = QLabel("ประเภทเอกสาร:")
        self.doc_type_combo = QComboBox()
        self.doc_type_combo.addItems([
            "หนังสือภายนอก",
            "หนังสือภายใน",
            "หนังสือประทับตรา"
        ])
        toolbar.addWidget(self.doc_type_label)
        toolbar.addWidget(self.doc_type_combo)

        # ปุ่มโหลดไฟล์
        self.load_button = QPushButton("เลือกไฟล์")
        self.load_button.clicked.connect(self.on_load_file)
        toolbar.addWidget(self.load_button)

        toolbar.addStretch()
        layout.addLayout(toolbar)

    def setup_event_handlers(self):
        """ตั้งค่า event handlers"""
        self.space_manager.subscribe_to_event('file_loaded', self.on_file_loaded)

    def on_load_file(self):
        """จัดการเมื่อกดปุ่มโหลดไฟล์"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "เลือกเอกสาร",
            "",
            "Documents (*.pdf *.jpg *.jpeg *.png)"
        )
        
        if file_name:
            # ส่ง event แจ้งว่ามีการโหลดไฟล์
            self.space_manager.publish_event('file_selected', {
                'file_path': file_name,
                'document_type': self.doc_type_combo.currentText()
            })

    def on_file_loaded(self, data):
        """จัดการเมื่อไฟล์ถูกโหลดเสร็จ"""
        # TODO: แสดงไฟล์ที่โหลด
        pass