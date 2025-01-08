from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt
from controllers.file_controller import FileController

class FileListView(QWidget):
    """Widget แสดงรายการไฟล์"""
    
    file_selected = pyqtSignal(str)  # ส่ง path ของไฟล์ที่เลือก
    
    def __init__(self, controller: FileController):
        super().__init__()
        self._controller = controller
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """สร้าง UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
    
    def _connect_signals(self):
        """เชื่อมต่อ signals"""
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self._controller.files_updated.connect(self.update_file_list)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """จัดการเมื่อคลิกเลือกไฟล์"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self._controller.select_file(file_path)
        self.file_selected.emit(file_path)
    
    def update_file_list(self, files: list):
        """อัพเดตรายการไฟล์"""
        self.list_widget.clear()
        for file in files:
            item = QListWidgetItem(file.display_name)
            item.setData(Qt.ItemDataRole.UserRole, file.path)
            self.list_widget.addItem(item)