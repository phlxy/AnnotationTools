# controllers/zoom_controller.py
from models.zoom_model import ZoomModel

class ZoomController:
    def __init__(self):
        self.zoom_model = ZoomModel()
        self.views = []  # เก็บ views ที่ต้องอัพเดทเมื่อมีการซูม

    def add_view(self, view):
        """เพิ่ม view ที่ต้องอัพเดทเมื่อซูม"""
        self.views.append(view)

    def zoom_in(self):
        """จัดการการซูมเข้า"""
        zoom = self.zoom_model.zoom_in()
        self._notify_views()
        return zoom

    def zoom_out(self):
        """จัดการการซูมออก"""
        zoom = self.zoom_model.zoom_out()
        self._notify_views()
        return zoom

    def reset_zoom(self):
        """จัดการการรีเซ็ตซูม"""
        zoom = self.zoom_model.reset_zoom()
        self._notify_views()
        return zoom

    def set_zoom(self, factor):
        """จัดการการกำหนดค่าซูม"""
        zoom = self.zoom_model.set_zoom(factor)
        self._notify_views()
        return zoom

    def get_zoom_factor(self):
        """รับค่า zoom factor ปัจจุบัน"""
        return self.zoom_model.zoom_factor

    def _notify_views(self):
        """แจ้งเตือน views ให้อัพเดท"""
        for view in self.views:
            view.update_zoom(self.zoom_model.get_zoom_percentage())