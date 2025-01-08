from PyQt6.QtCore import QObject, pyqtSignal

class ZoomModel(QObject):
    """Model สำหรับจัดการค่าและการคำนวณเกี่ยวกับ zoom"""
    
    zoom_changed = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        # ค่าคงที่
        self._MIN_ZOOM = 0.1
        self._MAX_ZOOM = 5.0
        self._ZOOM_STEP = 0.2
        
        # ค่าเริ่มต้น
        self._zoom_factor = 1.0
        
    @property
    def zoom_factor(self) -> float:
        return self._zoom_factor
    
    def zoom_in(self) -> None:
        """เพิ่มขนาด zoom"""
        new_zoom = min(self._zoom_factor + self._ZOOM_STEP, self._MAX_ZOOM)
        if new_zoom != self._zoom_factor:
            self._zoom_factor = new_zoom
            self.zoom_changed.emit(self._zoom_factor)
    
    def zoom_out(self) -> None:
        """ลดขนาด zoom"""
        new_zoom = max(self._zoom_factor - self._ZOOM_STEP, self._MIN_ZOOM)
        if new_zoom != self._zoom_factor:
            self._zoom_factor = new_zoom
            self.zoom_changed.emit(self._zoom_factor)
    
    def reset_zoom(self) -> None:
        """รีเซ็ต zoom เป็น 100%"""
        if self._zoom_factor != 1.0:
            self._zoom_factor = 1.0
            self.zoom_changed.emit(self._zoom_factor)
    
    def get_zoom_info(self) -> dict:
        """รวบรวมข้อมูลสถานะ zoom ทั้งหมด"""
        return {
            'factor': self._zoom_factor,
            'percent': int(self._zoom_factor * 100),
            'can_zoom_in': self._zoom_factor < self._MAX_ZOOM,
            'can_zoom_out': self._zoom_factor > self._MIN_ZOOM
        }

    def transform_point(self, x: float, y: float) -> tuple[float, float]:
        """แปลงพิกัดตามค่า zoom"""
        return x / self._zoom_factor, y / self._zoom_factor