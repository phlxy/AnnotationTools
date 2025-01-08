from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QComboBox, 
                            QFileDialog, QListWidget, QListWidgetItem, QScrollArea,QMessageBox)
from .toolbar_view import ToolbarView
from controllers.label_controller import LabelController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.controller = LabelController()
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("เครื่องมือ Annotation เอกสาร")
        self.setGeometry(100, 100, 1200, 800)
        
        # สร้าง widget หลัก
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # ปรับขนาด window
        self.setGeometry(100, 100, 1400, 1000)

        self.toolbar = ToolbarView()
        layout.addWidget(self.toolbar)
