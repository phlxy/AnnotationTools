import os
import json
from datetime import datetime
from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QMessageBox

class AutoSaver(QObject):
    def __init__(self, parent=None, autosave_interval=5):
        super().__init__(parent)
        
        self.autosave_interval = autosave_interval * 60 * 1000
        self.autosave_path = "autosave"
        self.last_save_time = datetime.now()
        self.has_unsaved_changes = False
        
        if not os.path.exists(self.autosave_path):
            os.makedirs(self.autosave_path)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_save)
        self.timer.start(self.autosave_interval)
        
        # ข้อมูลปัจจุบัน
        self.current_data = None

    def update_current_data(self, data):
        """อัพเดทข้อมูลปัจจุบัน"""
        self.current_data = data
        self.has_unsaved_changes = True

    def auto_save(self):
        """บันทึกข้อมูลอัตโนมัติ"""
        if not self.has_unsaved_changes or not self.current_data:
            return False

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            basename = os.path.splitext(os.path.basename(self.current_data['image_path']))[0]
            save_path = os.path.join(self.autosave_path, f"{basename}_autosave_{timestamp}.json")
            
            save_data = {
                **self.current_data,
                'timestamp': timestamp
            }
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
            self.has_unsaved_changes = False
            self.last_save_time = datetime.now()
            print(f"Auto-saved to: {save_path}")
            return True
            
        except Exception as e:
            print(f"Auto-save failed: {str(e)}")
            return False

    def check_for_autosave(self, image_path):
        """ตรวจสอบและโหลดไฟล์ autosave สำหรับรูปภาพ"""
        latest_autosave = self.get_latest_autosave(image_path)
        if not latest_autosave:
            return None

        try:
            with open(latest_autosave, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading autosave: {str(e)}")
            return None

    def get_latest_autosave(self, image_path):
        """ค้นหาไฟล์ autosave ล่าสุดของรูปภาพ"""
        if not os.path.exists(self.autosave_path) or not image_path:
            return None
            
        basename = os.path.splitext(os.path.basename(image_path))[0]
        autosave_files = [
            f for f in os.listdir(self.autosave_path)
            if f.startswith(basename) and f.endswith('.json')
        ]
        
        if not autosave_files:
            return None
        
        latest = max(autosave_files, key=lambda x: os.path.getmtime(
            os.path.join(self.autosave_path, x))
        )
        return os.path.join(self.autosave_path, latest)

    def cleanup_old_autosaves(self, max_files_per_image=5):
        """ลบไฟล์ autosave เก่า"""
        if not os.path.exists(self.autosave_path):
            return

        # จัดกลุ่มไฟล์ตามรูปภาพ
        autosaves_by_image = {}
        for filename in os.listdir(self.autosave_path):
            if not filename.endswith('.json'):
                continue
                
            base_name = filename.split('_autosave_')[0]
            if base_name not in autosaves_by_image:
                autosaves_by_image[base_name] = []
            
            full_path = os.path.join(self.autosave_path, filename)
            autosaves_by_image[base_name].append((
                full_path,
                os.path.getmtime(full_path)
            ))

        # ลบไฟล์เก่า
        for base_name, files in autosaves_by_image.items():
            if len(files) > max_files_per_image:
                sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
                for file_path, _ in sorted_files[max_files_per_image:]:
                    try:
                        os.remove(file_path)
                        print(f"Removed old autosave: {file_path}")
                    except Exception as e:
                        print(f"Failed to remove {file_path}: {str(e)}")
                        
    def set_autosave_interval(self, minutes):
        """ปรับเปลี่ยนช่วงเวลาการ auto-save"""
        self.autosave_interval = minutes * 60 * 1000
        self.timer.setInterval(self.autosave_interval)