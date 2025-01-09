# models/zoom_model.py
class ZoomModel:
    def __init__(self):
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0

    def zoom_in(self):
        """เพิ่มขนาดการซูม"""
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor = min(self.zoom_factor * 1.2, self.max_zoom)
        return self.zoom_factor

    def zoom_out(self):
        """ลดขนาดการซูม"""
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor = max(self.zoom_factor * 0.8, self.min_zoom)
        return self.zoom_factor

    def reset_zoom(self):
        """รีเซ็ตการซูม"""
        self.zoom_factor = 1.0
        return self.zoom_factor

    def set_zoom(self, factor):
        """กำหนดค่าการซูมโดยตรง"""
        self.zoom_factor = min(max(factor, self.min_zoom), self.max_zoom)
        return self.zoom_factor

    def get_zoom_percentage(self):
        """คำนวณเปอร์เซ็นต์การซูม"""
        return int(self.zoom_factor * 100)