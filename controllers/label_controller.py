from typing import List
from models.label_model import LabelModel
from PyQt6.QtCore import pyqtSignal, QObject

class LabelController(QObject):
    label_changed = pyqtSignal(str)
    document_type_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.label_model = LabelModel()
        print(f"[DEBUG] LabelController: Initialized with LabelModel.")

    def change_document_type(self, document_type: str):
        """เปลี่ยนประเภทเอกสารใน LabelModel"""
        print(f"[DEBUG] LabelController: Changing document type to '{document_type}'")
        self.label_model.set_document_type(document_type)
        self.document_type_changed.emit(document_type)

    def get_all_labels(self) -> List[str]:
        """ดึงรายการป้ายกำกับทั้งหมดจาก LabelModel"""
        labels = self.label_model.get_all_labels()
        print(f"[DEBUG] LabelController: Retrieved labels {labels}")
        return labels

    def set_current_label(self, label: str):
        """ตั้งค่าป้ายกำกับปัจจุบันใน LabelModel"""
        print(f"[DEBUG] LabelController: Setting current label to '{label}'")
        self.label_model.set_current_label(label)
        self.label_changed.emit(label)
