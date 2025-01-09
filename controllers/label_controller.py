import logging
from models.label_model import LabelModel
from PyQt6.QtCore import pyqtSignal, QObject

# ตั้งค่า logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class LabelController(QObject):
    """Controller for managing labels and document types."""
    
    # Signals สำหรับการสื่อสารกับ View
    label_changed = pyqtSignal(str)
    document_type_changed = pyqtSignal(str)

    def __init__(self):
        """Initialize LabelController with a LabelModel."""
        super().__init__()
        self.label_model = LabelModel()
        logging.debug("[LabelController] Initialized with LabelModel.")

    def change_document_type(self, document_type: str):
        """
        เปลี่ยนประเภทเอกสารใน LabelModel
        :param document_type: ประเภทเอกสารใหม่
        """
        logging.debug(f"[LabelController] Changing document type to '{document_type}'")
        self.label_model.set_document_type(document_type)
        self.document_type_changed.emit(document_type)
        logging.info(f"[LabelController] Document type changed to '{document_type}'")

    def get_all_labels(self):
        """
        ดึงรายการป้ายกำกับทั้งหมดจาก LabelModel
        :return: รายการป้ายกำกับ (List of labels)
        """
        labels = self.label_model.get_all_labels()
        logging.debug(f"[LabelController] Retrieved labels: {labels}")
        return labels

    def set_current_label(self, label: str):
        """
        ตั้งค่าป้ายกำกับปัจจุบันใน LabelModel
        :param label: ชื่อป้ายกำกับ
        """
        logging.debug(f"[LabelController] Setting current label to '{label}'")
        self.label_model.set_current_label(label)
        self.label_changed.emit(label)
        logging.info(f"[LabelController] Current label set to '{label}'")
