from typing import List, Optional
from PyQt6.QtCore import QObject, pyqtSignal
from models.file_model import FileModel, FileInfo

class FileController(QObject):
    """Controller สำหรับจัดการไฟล์"""
    
    # Signals
    file_loaded = pyqtSignal(str)        # ส่ง path ของไฟล์ที่โหลด
    files_updated = pyqtSignal(list)     # ส่งรายการไฟล์ที่อัพเดต
    error_occurred = pyqtSignal(str)     # ส่งข้อความ error
    
    def __init__(self):
        super().__init__()
        self._model = FileModel()
        
        # เชื่อมต่อ signals จาก model
        self._model.files_changed.connect(self._handle_files_changed)
        self._model.error_occurred.connect(self.error_occurred)
    
    def load_file(self, file_path: str) -> None:
        """
        โหลดไฟล์ใหม่
        
        Args:
            file_path: path ของไฟล์ที่จะโหลด
        """
        self._model.load_file(file_path)
    
    def select_file(self, file_path: str) -> None:
        """
        เลือกไฟล์จากรายการ
        
        Args:
            file_path: path ของไฟล์ที่เลือก
        """
        file_info = self._model.set_current_file(file_path)
        if file_info:
            self.file_loaded.emit(file_info.path)
    
    def get_current_file(self) -> Optional[FileInfo]:
        """รับข้อมูลไฟล์ปัจจุบัน"""
        return self._model.get_current_file()
    
    def get_all_files(self) -> List[FileInfo]:
        """รับรายการไฟล์ทั้งหมด"""
        return self._model.get_all_files()
    
    def _handle_files_changed(self, files: List[FileInfo]) -> None:
        """จัดการเมื่อรายการไฟล์เปลี่ยนแปลง"""
        self.files_updated.emit(files)