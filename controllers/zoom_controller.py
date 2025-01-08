from typing import Tuple
from PyQt6.QtCore import QObject, pyqtSignal
from models.zoom_model import ZoomModel

class ZoomController(QObject):
    """Controller class สำหรับจัดการการ zoom และเชื่อมต่อระหว่าง model กับ view"""
    
    zoom_status_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self._model = ZoomModel()
        self._model.zoom_changed.connect(self._handle_zoom_change)
    
    def _handle_zoom_change(self, factor: float) -> None:
        """
        จัดการเมื่อค่า zoom เปลี่ยน และส่งข้อมูลสถานะไปยัง view
        
        Args:
            factor (float): ค่า zoom factor ใหม่
        """
        status = self._model.get_zoom_info()
        self.zoom_status_updated.emit(status)
    
    def zoom_in(self) -> None:
        """สั่งให้เพิ่มขนาด zoom"""
        self._model.zoom_in()
    
    def zoom_out(self) -> None:
        """สั่งให้ลดขนาด zoom"""
        self._model.zoom_out()
    
    def reset_zoom(self) -> None:
        """สั่งให้รีเซ็ต zoom เป็น 100%"""
        self._model.reset_zoom()
    
    def handle_wheel_event(self, delta: int, ctrl_pressed: bool = False) -> None:
        """
        จัดการ event จากการหมุนล้อเมาส์
        
        Args:
            delta (int): ค่าการหมุน (บวกคือหมุนขึ้น, ลบคือหมุนลง)
            ctrl_pressed (bool): สถานะการกดปุ่ม Ctrl
        """
        if not ctrl_pressed:
            return
            
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    def transform_point(self, x: float, y: float) -> Tuple[float, float]:
        """
        แปลงพิกัดตามค่า zoom ปัจจุบัน
        
        Args:
            x (float): พิกัด x
            y (float): พิกัด y
            
        Returns:
            Tuple[float, float]: พิกัดที่แปลงแล้ว (x, y)
        """
        return self._model.transform_point(x, y)