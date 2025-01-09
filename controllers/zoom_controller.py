from models.zoom_model import ZoomModel
import logging

# ตั้งค่า logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class ZoomController:
    """Controller for managing zoom actions."""
    
    def __init__(self):
        """Initialize ZoomController with ZoomModel and associated views."""
        self.zoom_model = ZoomModel()
        self.views = []  # เก็บ views ที่ต้องอัพเดทเมื่อมีการซูม
        logging.debug("[ZoomController] Initialized with ZoomModel.")

    def add_view(self, view):
        """เพิ่ม view ที่ต้องอัพเดทเมื่อซูม."""
        self.views.append(view)
        logging.debug(f"[ZoomController] View added: {view}")

    def zoom_in(self):
        """จัดการการซูมเข้า."""
        logging.debug("[ZoomController] Zooming in.")
        zoom = self.zoom_model.zoom_in()
        self._notify_views()
        logging.info(f"[ZoomController] Zoomed in to {self.zoom_model.get_zoom_percentage()}%.")
        return zoom

    def zoom_out(self):
        """จัดการการซูมออก."""
        logging.debug("[ZoomController] Zooming out.")
        zoom = self.zoom_model.zoom_out()
        self._notify_views()
        logging.info(f"[ZoomController] Zoomed out to {self.zoom_model.get_zoom_percentage()}%.")
        return zoom

    def reset_zoom(self):
        """จัดการการรีเซ็ตซูม."""
        logging.debug("[ZoomController] Resetting zoom.")
        zoom = self.zoom_model.reset_zoom()
        self._notify_views()
        logging.info(f"[ZoomController] Zoom reset to {self.zoom_model.get_zoom_percentage()}%.")
        return zoom

    def set_zoom(self, factor):
        """จัดการการกำหนดค่าซูม."""
        logging.debug(f"[ZoomController] Setting zoom factor to {factor}.")
        zoom = self.zoom_model.set_zoom(factor)
        self._notify_views()
        logging.info(f"[ZoomController] Zoom factor set to {self.zoom_model.get_zoom_percentage()}%.")
        return zoom

    def get_zoom_factor(self):
        """รับค่า zoom factor ปัจจุบัน."""
        zoom_factor = self.zoom_model.zoom_factor
        logging.debug(f"[ZoomController] Current zoom factor: {zoom_factor}")
        return zoom_factor

    def _notify_views(self):
        """แจ้งเตือน views ให้อัพเดท."""
        zoom_percentage = self.zoom_model.get_zoom_percentage()
        logging.debug(f"[ZoomController] Notifying views with zoom percentage: {zoom_percentage}%.")
        for view in self.views:
            view.update_zoom(zoom_percentage)
