from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QFrame
from PyQt6.QtCore import Qt
from controllers.label_controller import LabelController
from config.config import Config

class LabelView(QWidget):
    def __init__(self, parent: QWidget, controller: LabelController):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout(self)  # Initialize the layout
        self.setLayout(self.layout)       # Set the layout for the widget

        # เพิ่ม Document Type Selector
        self.doc_type_label = QLabel("ประเภทเอกสาร:")
        self.layout.addWidget(self.doc_type_label)

        self.doc_type_combo = QComboBox()
        self.doc_type_combo.addItems(Config.DOCUMENT_TYPES.keys())
        self.doc_type_combo.setFixedWidth(150)
        self.layout.addWidget(self.doc_type_combo)

        # เชื่อมต่อสัญญาณเมื่อมีการเปลี่ยนแปลงประเภทเอกสาร
        self.doc_type_combo.currentTextChanged.connect(self.update_labels)

        # เพิ่ม separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setFixedHeight(20)
        self.layout.addWidget(separator)

        # Label Selector
        self.label_selector_label = QLabel("ป้ายกำกับ:")
        self.layout.addWidget(self.label_selector_label)

        self.label_combo = QComboBox()
        self.update_labels()  # เรียกใชานครั้งแรกเพื่อแสดงป้ายกำกับเริ่มต้น
        self.label_combo.currentTextChanged.connect(self.on_label_changed)
        self.layout.addWidget(self.label_combo)

    def update_labels(self):
        """อัพเดทรายการป้ายกำกับตามประเภทเอกสารที่เลือก"""
        doc_type = self.doc_type_combo.currentText()  # เลือกประเภทเอกสารจาก combobox
        print(f"[DEBUG] LabelView: Selected Document Type: {doc_type}")  # สำหรับการดีบัค

        self.controller.change_document_type(doc_type)  # เปลี่ยนประเภทเอกสารใน Model
        self.label_combo.clear()  # ลบรายการป้ายกำกับเก่า

        labels = self.controller.get_all_labels()  # ดึงป้ายกำกับใหม่จาก Model
        print(f"[DEBUG] LabelView: Retrieved Labels: {labels}")  # สำหรับการดีบัค

        self.label_combo.addItems(labels)  # อัพเดตป้ายกำกับใหม่

    def on_label_changed(self, label: str):
        """จัดการเมื่อเปลี่ยน label"""
        print(f"[DEBUG] LabelView: Selected Label: {label}")  # สำหรับการดีบัค
        self.controller.set_current_label(label)  # ตั้งค่าป้ายกำกับใน Model 
