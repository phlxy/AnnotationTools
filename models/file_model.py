from typing import List, Dict, Optional
from dataclasses import dataclass
from PyQt6.QtCore import QObject, pyqtSignal
import os
from pdf2image import convert_from_path

@dataclass
class FileInfo:
    """ข้อมูลของไฟล์เอกสาร"""
    path: str                # path ของไฟล์
    display_name: str        # ชื่อที่แสดงในรายการ
    file_type: str          # ประเภทไฟล์ (pdf/image)
    page_number: int = 1    # เลขหน้า (สำหรับ PDF)
    original_path: str = "" # path ต้นฉบับ (สำหรับไฟล์ที่แปลงมา)

class FileModel(QObject):
    """Model สำหรับจัดการไฟล์เอกสาร"""
    
    files_changed = pyqtSignal(list)  # ส่งรายการไฟล์ที่อัพเดต
    error_occurred = pyqtSignal(str)  # ส่งข้อความ error
    
    def __init__(self, temp_dir: str = "temp_images"):
        super().__init__()
        self._temp_dir = temp_dir
        self._files: List[FileInfo] = []
        self._current_file: Optional[FileInfo] = None
        
        # สร้างโฟลเดอร์ temp ถ้ายังไม่มี
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
    
    def load_file(self, file_path: str) -> None:
        """
        โหลดไฟล์เข้าระบบ
        
        Args:
            file_path: path ของไฟล์ที่จะโหลด
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                self._load_pdf(file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                self._load_image(file_path)
            else:
                self.error_occurred.emit(f"ไม่รองรับไฟล์นามสกุล {file_ext}")
                return
                
            self.files_changed.emit(self._files)
            
        except Exception as e:
            self.error_occurred.emit(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {str(e)}")
    
    def _load_pdf(self, pdf_path: str) -> None:
        """แปลง PDF เป็นรูปภาพและเพิ่มเข้ารายการ"""
        basename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.join(self._temp_dir, basename)
        
        # สร้างโฟลเดอร์สำหรับเก็บรูปภาพ
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # แปลง PDF เป็นรูปภาพ
        pages = convert_from_path(pdf_path)
        
        for i, page in enumerate(pages, 1):
            image_path = os.path.join(output_dir, f"page_{i}.jpg")
            page.save(image_path, "JPEG")
            
            self._files.append(FileInfo(
                path=image_path,
                display_name=f"{basename} - หน้า {i}",
                file_type='pdf_page',
                page_number=i,
                original_path=pdf_path
            ))
    
    def _load_image(self, image_path: str) -> None:
        """เพิ่มไฟล์รูปภาพเข้ารายการ"""
        basename = os.path.basename(image_path)
        self._files.append(FileInfo(
            path=image_path,
            display_name=basename,
            file_type='image',
            original_path=image_path
        ))
    
    def set_current_file(self, file_path: str) -> Optional[FileInfo]:
        """
        ตั้งค่าไฟล์ปัจจุบัน
        
        Args:
            file_path: path ของไฟล์ที่ต้องการ
            
        Returns:
            FileInfo ของไฟล์ที่เลือก หรือ None ถ้าไม่พบ
        """
        for file in self._files:
            if file.path == file_path:
                self._current_file = file
                return file
        return None
    
    def get_current_file(self) -> Optional[FileInfo]:
        """รับข้อมูลไฟล์ปัจจุบัน"""
        return self._current_file
    
    def get_all_files(self) -> List[FileInfo]:
        """รับรายการไฟล์ทั้งหมด"""
        return self._files
    
    def cleanup(self) -> None:
        """ลบไฟล์ชั่วคราวทั้งหมด"""
        import shutil
        if os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)