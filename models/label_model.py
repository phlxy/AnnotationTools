from typing import Dict, List
from config.config import Config
import logging

class LabelModel:
    def __init__(self, initial_document_type: str = None):
        self.document_type = initial_document_type or (next(iter(Config.DOCUMENT_TYPES), ""))
        self.labels = self._get_labels()
        self.current_label = next(iter(self.labels), None)
        print(f"[DEBUG] LabelModel: Initialized with document type '{self.document_type}' and labels {self.labels}")

    def _get_labels(self) -> Dict[str, str]:
        """รับ labels สำหรับประเภทเอกสาร"""
        labels = Config.DOCUMENT_TYPES.get(self.document_type, {})
        print(f"[DEBUG] LabelModel: Fetched labels {labels} for document type '{self.document_type}'")
        return labels

    def set_document_type(self, document_type: str):
        """เปลี่ยนประเภทเอกสาร"""
        self.document_type = document_type
        self.labels = self._get_labels()
        self.current_label = next(iter(self.labels), None)
        print(f"[DEBUG] LabelModel: Document type set to '{self.document_type}', current label '{self.current_label}'")

    def get_color(self, label: str) -> str:
        """รับสีของ label"""
        color = self.labels.get(label, '#000000')
        print(f"[DEBUG] LabelModel: Color for label '{label}' is '{color}'")
        return color

    def get_all_labels(self) -> List[str]:
        """รับรายการ labels ทั้งหมด"""
        labels = list(self.labels.keys())
        print(f"[DEBUG] LabelModel: All labels are {labels}")
        return labels

    def set_current_label(self, label: str):
        """กำหนด label ปัจจุบัน"""
        if label in self.labels:
            self.current_label = label
            print(f"[DEBUG] LabelModel: Current label set to '{self.current_label}'")
        else:
            logging.warning(f"Attempted to set invalid label: {label}")
            print(f"[WARNING] LabelModel: Attempted to set invalid label '{label}'")
