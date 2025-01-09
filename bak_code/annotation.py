import sys
import json
import os
from validator import AnnotationValidator
from autosaver import AutoSaver
from document_loader import DocumentLoader
from PyQt6.QtWidgets import QSplitter
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QComboBox, 
                            QFileDialog, QListWidget, QListWidgetItem, QScrollArea,QMessageBox)
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt

class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("เครื่องมือ Annotation เอกสาร")
        self.setGeometry(100, 100, 1200, 800)

        # เพิ่มตัวแปรใหม่ใน __init__
        self.file_annotations = {}  # เก็บ annotations แยกตามไฟล์

        # ตัวแปรสำหรับการวาด
        self.image_path = None
        self.original_pixmap = None
        self.scaled_pixmap = None
        self.drawing = False
        self.start_point = None
        self.current_box = None
        self.annotations = []
        self.scale_factor = 1.0

        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
        # กำหนด labels และสี
        self.labels = {
            'ข้อความ': '#FF0000',
            'หัวเรื่อง': '#00FF00',
            'ลายเซ็น': '#0000FF',
            'ตราประทับ': '#FFFF00',
            'ตาราง': '#FF00FF',
            'วันที่': '#00FFFF',
            'เลขที่หนังสือ': '#FF8800'
        }
        # เพิ่มคำอธิบายสำหรับแต่ละ label ตามประเภทเอกสาร
        self.label_descriptions = {
            "หนังสือภายนอก": {
                'ที่': 'รหัสหนังสือราชการ (เช่น มท 0123.4/123)',
                'ส่วนราชการ': 'ชื่อส่วนราชการเจ้าของหนังสือ และที่ตั้ง',
                'วันที่': 'วันที่ออกหนังสือ (เช่น 1 มกราคม 2567)',
                'เรื่อง': 'ชื่อเรื่องของหนังสือ',
                'เรียน': 'ตำแหน่งของผู้รับหนังสือ',
                'อ้างถึง': 'หนังสือที่เคยติดต่อกันก่อนหน้า (ถ้ามี)',
                'สิ่งที่ส่งมาด้วย': 'เอกสารที่แนบมาพร้อมกับหนังสือ (ถ้ามี)',
                'เนื้อความ': 'ส่วนเนื้อหาของหนังสือ',
                'ลงชื่อ': 'ลายมือชื่อผู้ลงนามในหนังสือ',
                'ตำแหน่ง': 'ตำแหน่งของผู้ลงนาม'
            },
            "หนังสือภายใน": {
                'ส่วนราชการ': 'ส่วนราชการเจ้าของเรื่อง',
                'ที่': 'รหัสหนังสือภายใน',
                'วันที่': 'วันที่ที่ออกหนังสือ',
                'เรื่อง': 'ชื่อเรื่องของบันทึก',
                'เรียน': 'ตำแหน่งของผู้รับบันทึก',
                'เนื้อความ': 'รายละเอียดของเรื่องที่ต้องการเสนอ',
                'ลงชื่อ': 'ลายมือชื่อผู้บันทึก',
                'ตำแหน่ง': 'ตำแหน่งของผู้บันทึก'
            },
            "หนังสือประทับตรา": {
                'ที่': 'รหัสหนังสือประทับตรา',
                'ถึง': 'หน่วยงานหรือบุคคลที่รับหนังสือ',
                'เรื่อง': 'ชื่อเรื่องของหนังสือ',
                'ตราประทับ': 'ตราชื่อส่วนราชการ',
                'วันที่': 'วันที่ที่ออกหนังสือ',
                'เนื้อความ': 'ข้อความของหนังสือ'
            }
        }
        # เพิ่ม labels ตามประเภทเอกสาร
        self.document_labels = {
            "หนังสือภายนอก": {
                'ที่': '#FF0000',
                'ส่วนราชการ': '#00FF00',
                'วันที่': '#0000FF',
                'เรื่อง': '#FFFF00',
                'เรียน': '#FF00FF',
                'อ้างถึง': '#00FFFF',
                'สิ่งที่ส่งมาด้วย': '#FF8800',
                'เนื้อความ': '#808080',
                'ลงชื่อ': '#008080',
                'ตำแหน่ง': '#800080'
            },
            "หนังสือภายใน": {
                'ส่วนราชการ': '#FF0000',
                'ที่': '#00FF00',
                'วันที่': '#0000FF',
                'เรื่อง': '#FFFF00',
                'เรียน': '#FF00FF',
                'เนื้อความ': '#808080',
                'ลงชื่อ': '#008080',
                'ตำแหน่ง': '#800080'
            },
            # เพิ่มประเภทอื่นๆ ตามต้องการ
        }

        # เริ่มต้นด้วยหนังสือภายนอก
        self.labels = self.document_labels["หนังสือภายนอก"]
        # เพิ่ม validator
        self.validator = AnnotationValidator(self.label_descriptions)
        # เพิ่ม AutoSaver
        self.autosaver = AutoSaver(self)
        # เพิ่ม document loader
        self.doc_loader = DocumentLoader()
        
        # ตัวแปรเก็บข้อมูลเอกสาร
        self.current_document = None  # เก็บข้อมูลเอกสารปัจจุบัน
        self.file_annotations = {}    # เก็บ annotations แยกตามไฟล์
        self.setup_ui()

    def setup_ui(self):
        # สร้าง widget หลัก
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # ปรับขนาด window
        self.setGeometry(100, 100, 1400, 1000)

        # Toolbar ชุดแรก
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 10)

        # เพิ่ม Document Type Selector
        self.doc_type_label = QLabel("ประเภทเอกสาร:")
        self.doc_type_combo = QComboBox()
        self.doc_type_combo.addItems([
            "หนังสือภายนอก",
            "หนังสือภายใน",
            "หนังสือประทับตรา",
            "คำสั่ง",
            "ระเบียบ",
            "ประกาศ"
        ])
        self.doc_type_combo.setFixedWidth(150)
        toolbar.addWidget(self.doc_type_label)
        toolbar.addWidget(self.doc_type_combo)

        # เพิ่ม separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        toolbar.addWidget(separator)

        # ปุ่มโหลดไฟล์
        self.load_button = QPushButton("เลือกไฟล์")
        self.load_button.clicked.connect(self.load_image)
        self.load_button.setFixedWidth(100)
        toolbar.addWidget(self.load_button)

        # ปุ่มโหลดหลายไฟล์
        self.load_batch_button = QPushButton("เพิ่มหลายไฟล์")
        self.load_batch_button.clicked.connect(self.load_batch_files)
        self.load_batch_button.setFixedWidth(100)
        toolbar.addWidget(self.load_batch_button)

        self.label_combo = QComboBox()
        self.label_combo.addItems(self.labels.keys())
        self.label_combo.setFixedWidth(150)
        toolbar.addWidget(self.label_combo)

        # ปุ่ม zoom
        self.zoom_out_button = QPushButton("🔍-")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setFixedWidth(50)
        toolbar.addWidget(self.zoom_out_button)

        self.zoom_reset_button = QPushButton("100%")
        self.zoom_reset_button.clicked.connect(self.zoom_reset)
        self.zoom_reset_button.setFixedWidth(60)
        toolbar.addWidget(self.zoom_reset_button)

        self.zoom_in_button = QPushButton("🔍+")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setFixedWidth(50)
        toolbar.addWidget(self.zoom_in_button)

        self.undo_button = QPushButton("ย้อนกลับ")
        self.undo_button.clicked.connect(self.undo_last)
        self.undo_button.setFixedWidth(100)
        toolbar.addWidget(self.undo_button)

        # แทนปุ่ม export เดิม
        self.export_menu = QComboBox()
        self.export_menu.addItems(["JSON ปกติ", "LayoutLM Format"])
        self.export_menu.setFixedWidth(120)
        toolbar.addWidget(self.export_menu)

        self.export_button = QPushButton("ส่งออก")
        self.export_button.clicked.connect(self.export_by_format)
        self.export_button.setFixedWidth(100)
        toolbar.addWidget(self.export_button)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.save_button = QPushButton("บันทึก")
        self.save_button.clicked.connect(self.save_current_annotations)
        self.save_button.setFixedWidth(100)
        toolbar.addWidget(self.save_button)

        # สร้าง widget หลักสำหรับเนื้อหา
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)

        # เพิ่มรายการไฟล์ด้านซ้าย
        self.file_list_widget = QListWidget()
        self.file_list_widget.setMaximumWidth(300)
        self.file_list_widget.itemClicked.connect(self.load_selected_file)
        content_layout.addWidget(self.file_list_widget)

        # สร้าง splitter สำหรับแบ่งพื้นที่ระหว่างภาพและรายการ
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Scroll Area สำหรับภาพ
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(800)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_area.setWidget(self.image_label)
        
        # เพิ่ม scroll area เข้า splitter
        splitter.addWidget(scroll_area)
        
        # รายการ annotations
        annotation_widget = QWidget()
        annotation_layout = QVBoxLayout(annotation_widget)
        
        header_label = QLabel("รายการ Annotations:")
        header_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        annotation_layout.addWidget(header_label)
        
        self.annotation_list = QListWidget()
        self.annotation_list.setMaximumHeight(150)
        self.annotation_list.itemDoubleClicked.connect(self.delete_annotation)
        annotation_layout.addWidget(self.annotation_list)
        
        splitter.addWidget(annotation_widget)
        splitter.setSizes([800, 200])
        
        # เพิ่ม splitter เข้าใน content_layout
        content_layout.addWidget(splitter, stretch=1)
        
        # เพิ่ม content_widget เข้าใน layout หลัก
        layout.addWidget(content_widget)

        # เพิ่ม signal handler สำหรับการเปลี่ยนประเภทเอกสาร
        self.doc_type_combo.currentTextChanged.connect(self.update_labels_for_document_type)
        # หลังจากสร้าง combo boxes
        self.setup_label_tooltips()
        # เพิ่มปุ่มตรวจสอบก่อนปุ่ม export
        self.validate_button = QPushButton("ตรวจสอบ")
        self.validate_button.clicked.connect(self.validate_current)
        self.validate_button.setFixedWidth(100)
        toolbar.addWidget(self.validate_button)
        # ปรับปรุงปุ่มโหลดไฟล์
        load_button = QPushButton("เลือกเอกสาร")
        load_button.clicked.connect(self.load_document)
        toolbar.addWidget(load_button)

    def load_document(self):
        """โหลดเอกสาร (PDF หรือรูปภาพ)"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "เลือกเอกสาร",
            "",
            "Documents (*.pdf *.jpg *.jpeg *.png)"
        )
        
        if file_name:
            try:
                # บันทึก annotations ปัจจุบันก่อน
                if self.image_path and self.annotations:
                    self.save_current_annotations()
                    # อัพเดท autosaver
                    self.autosaver.update_current_data({
                        'image_path': self.image_path,
                        'document_type': self.doc_type_combo.currentText(),
                        'annotations': self.annotations,
                        'image_size': {
                            'width': self.original_pixmap.width(),
                            'height': self.original_pixmap.height()
                        }
                    })

                # โหลดเอกสารใหม่
                self.current_document = {
                    'path': file_name,
                    'pages': self.doc_loader.load_document(file_name)
                }
                
                # เคลียร์รายการไฟล์เก่า
                self.file_list_widget.clear()
                
                # เพิ่มรายการไฟล์ใหม่
                for page in self.current_document['pages']:
                    if page['type'] == 'pdf_page':
                        display_name = f"หน้า {page['page']}"
                    else:
                        display_name = os.path.basename(page['path'])
                        
                    item = QListWidgetItem(display_name)
                    item.setData(Qt.ItemDataRole.UserRole, page)
                    self.file_list_widget.addItem(item)
                
                # โหลด autosave ถ้ามี
                autosave_data = self.autosaver.check_for_autosave(file_name)
                if autosave_data:
                    reply = QMessageBox.question(
                        self,
                        'พบข้อมูลที่บันทึกอัตโนมัติ',
                        'ต้องการโหลดข้อมูลที่บันทึกอัตโนมัติหรือไม่?',
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        self.annotations = autosave_data['annotations']
                        self.doc_type_combo.setCurrentText(autosave_data['document_type'])
                        self.file_annotations[file_name] = self.annotations.copy()
                
            except Exception as e:
                QMessageBox.warning(self, "ข้อผิดพลาด", f"ไม่สามารถโหลดเอกสารได้: {str(e)}")

    def load_selected_file(self, item):
        """โหลดไฟล์ที่เลือกจากรายการ"""
        try:
            # บันทึก annotations ปัจจุบันก่อน
            if self.image_path and self.annotations:
                self.file_annotations[self.image_path] = self.annotations.copy()
                # อัพเดท autosaver
                self.autosaver.update_current_data({
                    'image_path': self.image_path,
                    'document_type': self.doc_type_combo.currentText(),
                    'annotations': self.annotations,
                    'image_size': {
                        'width': self.original_pixmap.width(),
                        'height': self.original_pixmap.height()
                    }
                })

            # ดึงข้อมูลที่เก็บไว้ใน item
            page_data = item.data(Qt.ItemDataRole.UserRole)
            
            if isinstance(page_data, str):
                self.image_path = page_data
            elif isinstance(page_data, dict):
                self.image_path = page_data['path']
            else:
                return
            
            # โหลดภาพ
            image = QImage(self.image_path)
            if image.isNull():
                QMessageBox.warning(self, "ข้อผิดพลาด", "ไม่สามารถโหลดรูปภาพได้")
                return
                
            self.original_pixmap = QPixmap.fromImage(image)
            
            # โหลด annotations ที่มีอยู่
            if self.image_path in self.file_annotations:
                self.annotations = self.file_annotations[self.image_path].copy()
            else:
                # ตรวจสอบ autosave
                autosave_data = self.autosaver.check_for_autosave(self.image_path)
                if autosave_data:
                    reply = QMessageBox.question(
                        self,
                        'พบข้อมูลที่บันทึกอัตโนมัติ',
                        'ต้องการโหลดข้อมูลที่บันทึกอัตโนมัติหรือไม่?',
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.Yes:
                        self.annotations = autosave_data['annotations']
                        # อัพเดทข้อมูลใน autosaver
                        self.autosaver.update_current_data(autosave_data)
                    else:
                        self.annotations = []
                else:
                    self.annotations = []
            
            self.update_annotation_list()
            self.show_image()
            
        except Exception as e:
            print(f"Error in load_selected_file: {str(e)}")
            QMessageBox.warning(self, "ข้อผิดพลาด", f"ไม่สามารถโหลดไฟล์ได้: {str(e)}")

    def export_layoutlm_format(self, directory):
        """Export ในรูปแบบที่ใช้กับ LayoutLMv3"""
        if self.current_document:
            for page in self.current_document['pages']:
                image_path = page['path']
                if image_path in self.file_annotations:
                    annotations = self.file_annotations[image_path]
                    
                    # สร้างชื่อไฟล์
                    if page['type'] == 'pdf_page':
                        basename = f"{os.path.splitext(os.path.basename(page['original_path']))[0]}_page_{page['page']}"
                    else:
                        basename = os.path.splitext(os.path.basename(page['original_path']))[0]
                        
                    json_name = f"{basename}_layoutlm.json"
                    save_path = os.path.join(directory, json_name)

                    # เตรียมข้อมูลสำหรับ LayoutLM
                    layoutlm_data = {
                        'image_path': image_path,
                        'original_path': page['original_path'],
                        'page_number': page.get('page', 1),
                        'document_type': self.doc_type_combo.currentText(),
                        'width': self.original_pixmap.width() if self.original_pixmap else None,
                        'height': self.original_pixmap.height() if self.original_pixmap else None,
                        'layout': {
                            'bbox': [],        # [x1, y1, x2, y2] coordinates
                            'label': [],       # label ของแต่ละ bbox
                            'words': [],       # text ในแต่ละ box (สำหรับ OCR)
                            'segment_ids': [],  # group ID สำหรับ boxes ที่เกี่ยวข้องกัน
                            'confidence': []   # ค่าความเชื่อมั่น
                        }
                    }

                    # แปลง annotations เป็น format ของ LayoutLM
                    for ann in annotations:
                        coords = ann['coordinates']
                        # แปลงพิกัดเป็น list ตามที่ LayoutLM ต้องการ
                        bbox = [
                            coords['x1'],   # x1
                            coords['y1'],   # y1
                            coords['x2'],   # x2
                            coords['y2']    # y2
                        ]
                        
                        layoutlm_data['layout']['bbox'].append(bbox)
                        layoutlm_data['layout']['label'].append(ann['label'])
                        layoutlm_data['layout']['words'].append("")  # เว้นว่างไว้สำหรับ OCR
                        layoutlm_data['layout']['segment_ids'].append(0)  # default group
                        layoutlm_data['layout']['confidence'].append(1.0)  # default confidence

                    # บันทึกไฟล์
                    with open(save_path, 'w', encoding='utf-8') as f:
                        json.dump(layoutlm_data, f, ensure_ascii=False, indent=2)

    def closeEvent(self, event):
        """เพิ่มการลบไฟล์ชั่วคราว"""
        self.doc_loader.cleanup()
        event.accept()

    def update_labels_for_document_type(self, document_type):
        """อัพเดท labels เมื่อเลือกประเภทเอกสารใหม่"""
        if document_type in self.document_labels:
            self.labels = self.document_labels[document_type]
            # อัพเดท combo box
            self.label_combo.clear()
            self.label_combo.addItems(self.labels.keys())
            # เพิ่ม tooltips
            self.setup_label_tooltips()

    def zoom_in(self):
        """เพิ่มขนาดภาพ"""
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor = min(self.zoom_factor * 1.2, self.max_zoom)
            self.update_image()
            self.update_zoom_buttons()

    def zoom_out(self):
        """ลดขนาดภาพ"""
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor = max(self.zoom_factor * 0.8, self.min_zoom)
            self.update_image()
            self.update_zoom_buttons()

    def zoom_reset(self):
        """รีเซ็ตขนาดภาพเป็น 100%"""
        self.zoom_factor = 1.0
        self.update_image()
        self.update_zoom_buttons()

    def update_zoom_buttons(self):
        """อัพเดทสถานะปุ่ม zoom"""
        self.zoom_out_button.setEnabled(self.zoom_factor > self.min_zoom)
        self.zoom_in_button.setEnabled(self.zoom_factor < self.max_zoom)
        self.zoom_reset_button.setText(f"{int(self.zoom_factor * 100)}%")

    def setup_label_tooltips(self):
        """เพิ่ม tooltips ให้กับ labels"""
        current_type = self.doc_type_combo.currentText()
        if current_type in self.label_descriptions:
            descriptions = self.label_descriptions[current_type]
            for i in range(self.label_combo.count()):
                label = self.label_combo.itemText(i)
                if label in descriptions:
                    self.label_combo.setItemData(
                        i, 
                        descriptions[label], 
                        Qt.ItemDataRole.ToolTipRole
                    )

    # เพิ่ม wheel event สำหรับ zoom ด้วยเมาส์
    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)


    def load_image(self):
        """โหลดเอกสาร (PDF หรือรูปภาพ)"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "เลือกเอกสาร",
            "",
            "Documents (*.pdf *.jpg *.jpeg *.png)"
        )
        
        if file_name:
            try:
                # โหลดเอกสาร
                self.current_document = {
                    'path': file_name,
                    'pages': self.doc_loader.load_document(file_name)
                }
                
                # เคลียร์รายการไฟล์เก่า
                self.file_list_widget.clear()
                
                # เพิ่มรายการไฟล์ใหม่
                for page in self.current_document['pages']:
                    if page['type'] == 'pdf_page':
                        display_name = f"หน้า {page['page']}"
                    else:
                        display_name = os.path.basename(page['path'])
                        
                    item = QListWidgetItem(display_name)
                    item.setData(Qt.ItemDataRole.UserRole, page)
                    self.file_list_widget.addItem(item)
                
            except Exception as e:
                QMessageBox.warning(self, "ข้อผิดพลาด", f"ไม่สามารถโหลดเอกสารได้: {str(e)}")

    def show_image(self):
        """แสดงภาพพร้อมปรับขนาด"""
        if self.original_pixmap:
            # คำนวณขนาดที่เหมาะสมสำหรับการแสดงผล
            label_size = self.image_label.size()
            scaled_size = self.original_pixmap.size()
            
            # ปรับขนาดตาม zoom factor
            scaled_width = int(scaled_size.width() * self.zoom_factor)
            scaled_height = int(scaled_size.height() * self.zoom_factor)
            
            self.scaled_pixmap = self.original_pixmap.scaled(
                scaled_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.image_label.setPixmap(self.scaled_pixmap)

    def get_image_coordinates(self, pos):
        """แปลงพิกัดเมาส์เป็นพิกัดจริงบนภาพ"""
        if not self.scaled_pixmap:
            return None

        # หาพิกัดของ label เทียบกับ window
        label_pos = self.image_label.mapTo(self, QPoint(0, 0))
        
        # หาพิกัดของภาพที่แสดงใน label
        label_rect = self.image_label.rect()
        pixmap_rect = self.scaled_pixmap.rect()
        
        # คำนวณ offset ของภาพที่ถูก center ใน label
        x_offset = (label_rect.width() - pixmap_rect.width()) // 2
        y_offset = (label_rect.height() - pixmap_rect.height()) // 2
        
        # คำนวณพิกัดเทียบกับภาพที่แสดง
        image_x = pos.x() - label_pos.x() - x_offset
        image_y = pos.y() - label_pos.y() - y_offset
        
        # แปลงกลับเป็นพิกัดบนภาพต้นฉบับ
        original_x = int(image_x / self.zoom_factor)
        original_y = int(image_y / self.zoom_factor)
        
        # ตรวจสอบว่าอยู่ในขอบเขตของภาพ
        original_x = max(0, min(original_x, self.original_pixmap.width() - 1))
        original_y = max(0, min(original_y, self.original_pixmap.height() - 1))
        
        return QPoint(original_x, original_y)

    def mousePressEvent(self, event):
        """จัดการการกดเมาส์"""
        if not self.original_pixmap:
            return
            
        # หา label position
        label_pos = self.image_label.mapTo(self, QPoint(0, 0))
        label_rect = QRect(label_pos, self.image_label.size())
        
        # ตรวจสอบว่าคลิกอยู่ในพื้นที่ของภาพ
        if label_rect.contains(event.pos()):
            mouse_pos = self.get_image_coordinates(event.pos())
            if mouse_pos:
                self.drawing = True
                self.start_point = mouse_pos

    def mouseMoveEvent(self, event):
        """จัดการการเคลื่อนที่ของเมาส์"""
        if not self.drawing or not self.original_pixmap:
            return
            
        mouse_pos = self.get_image_coordinates(event.pos())
        if mouse_pos and self.start_point:
            self.current_box = QRect(self.start_point, mouse_pos).normalized()
            self.update_image()

    def mouseReleaseEvent(self, event):
        """อัพเดทเมื่อมีการวาด annotation ใหม่"""
        if not self.drawing or not self.original_pixmap:
            return
            
        mouse_pos = self.get_image_coordinates(event.pos())
        if mouse_pos and self.start_point:
            rect = QRect(self.start_point, mouse_pos).normalized()
            
            if rect.width() > 5 and rect.height() > 5:
                self.annotations.append({
                    'label': self.label_combo.currentText(),
                    'coordinates': {
                        'x1': rect.left(),
                        'y1': rect.top(),
                        'x2': rect.right(),
                        'y2': rect.bottom()
                    }
                })
                self.update_annotation_list()
                
                # อัพเดท autosaver
                self.autosaver.update_current_data({
                    'image_path': self.image_path,
                    'document_type': self.doc_type_combo.currentText(),
                    'annotations': self.annotations,
                    'image_size': {
                        'width': self.original_pixmap.width(),
                        'height': self.original_pixmap.height()
                    }
                })
        
        self.drawing = False
        self.current_box = None
        self.update_image()


    def update_image(self):
        """อัพเดทการแสดงภาพพร้อมกับ annotations โดยคำนึงถึง zoom factor"""
        if not self.original_pixmap:
            return

        # คำนวณขนาดที่ต้องการหลัง zoom
        orig_width = self.original_pixmap.width()
        orig_height = self.original_pixmap.height()
        scaled_width = int(orig_width * self.zoom_factor)
        scaled_height = int(orig_height * self.zoom_factor)

        # สร้าง scaled pixmap
        temp_pixmap = self.original_pixmap.scaled(
            scaled_width,
            scaled_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # วาด annotations บน scaled pixmap
        painter = QPainter(temp_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # วาด annotations ที่มีอยู่
        for ann in self.annotations:
            color = QColor(self.labels[ann['label']])
            painter.setPen(QPen(color, max(1, int(3 * self.zoom_factor)), Qt.PenStyle.SolidLine))
            
            # ปรับพิกัดตาม zoom
            x1 = int(ann['coordinates']['x1'] * self.zoom_factor)
            y1 = int(ann['coordinates']['y1'] * self.zoom_factor)
            x2 = int(ann['coordinates']['x2'] * self.zoom_factor)
            y2 = int(ann['coordinates']['y2'] * self.zoom_factor)
            
            # วาดกรอบ
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)
            
            # เพิ่มการแสดง label
            font = painter.font()
            font.setPointSize(max(8, int(10 * self.zoom_factor)))  # ปรับขนาดตัวอักษรตาม zoom
            painter.setFont(font)
            
            # วาดพื้นหลังสำหรับ label
            text_rect = painter.fontMetrics().boundingRect(ann['label'])
            bg_rect = QRect(x1, y1 - text_rect.height(), text_rect.width() + 10, text_rect.height())
            painter.fillRect(bg_rect, QColor(255, 255, 255, 200))  # พื้นหลังสีขาวโปร่งใส
            
            # วาด label
            painter.drawText(x1 + 5, y1 - 5, ann['label'])

        # วาดกรอบปัจจุบัน (ถ้ามี)
        if self.current_box:
            current_label = self.label_combo.currentText()
            color = QColor(self.labels[current_label])
            painter.setPen(QPen(color, max(1, int(3 * self.zoom_factor)), Qt.PenStyle.SolidLine))
            
            # ปรับพิกัดของกรอบปัจจุบันตาม zoom
            x = int(self.current_box.x() * self.zoom_factor)
            y = int(self.current_box.y() * self.zoom_factor)
            w = int(self.current_box.width() * self.zoom_factor)
            h = int(self.current_box.height() * self.zoom_factor)
            
            # วาดกรอบ
            painter.drawRect(x, y, w, h)
            
            # วาด label สำหรับกรอบปัจจุบัน
            font = painter.font()
            font.setPointSize(max(8, int(10 * self.zoom_factor)))
            painter.setFont(font)
            
            # วาดพื้นหลังสำหรับ label
            text_rect = painter.fontMetrics().boundingRect(current_label)
            bg_rect = QRect(x, y - text_rect.height(), text_rect.width() + 10, text_rect.height())
            painter.fillRect(bg_rect, QColor(255, 255, 255, 200))
            
            # วาด label
            painter.drawText(x + 5, y - 5, current_label)

        painter.end()
        
        # อัพเดท scaled pixmap
        self.scaled_pixmap = temp_pixmap
        self.image_label.setPixmap(self.scaled_pixmap)

    def update_annotation_list(self):
        self.annotation_list.clear()
        for idx, ann in enumerate(self.annotations):
            coords = ann['coordinates']
            item_text = f"{idx + 1}. {ann['label']}: ({coords['x1']}, {coords['y1']}) - ({coords['x2']}, {coords['y2']})"
            self.annotation_list.addItem(item_text)

    def delete_annotation(self, item):
        """อัพเดทเมื่อลบ annotation"""
        idx = self.annotation_list.row(item)
        if idx >= 0:
            self.annotations.pop(idx)
            self.update_annotation_list()
            self.update_image()
            
            # แจ้ง AutoSaver
            self.autosaver.update_current_data(
                annotations=self.annotations
            )

    def undo_last(self):
        if self.annotations:
            self.annotations.pop()
            self.update_annotation_list()
            self.update_image()

    def load_batch_files(self):
        """โหลดหลายไฟล์พร้อมกัน"""
        file_names, _ = QFileDialog.getOpenFileNames(
            self, "เลือกไฟล์ภาพ", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        
        for file_name in file_names:
            item = QListWidgetItem(os.path.basename(file_name))
            # เก็บข้อมูลแบบ dictionary
            item_data = {
                'path': file_name,
                'type': 'image',
                'page': 1,
                'original_path': file_name
            }
            item.setData(Qt.ItemDataRole.UserRole, item_data)
            self.file_list_widget.addItem(item)


    def load_image_from_path(self, file_path):
        """โหลดภาพจาก path"""
        self.image_path = file_path
        image = QImage(file_path)
        self.original_pixmap = QPixmap.fromImage(image)
        self.show_image()
        self.annotations = []
        self.update_annotation_list()

    def save_current_annotations(self):
        """บันทึก annotations ของไฟล์ปัจจุบัน"""
        if self.image_path:
            self.file_annotations[self.image_path] = self.annotations.copy()
 

    def export_annotations(self, directory):
        """export แบบ JSON ปกติ"""
        for image_path, annotations in self.file_annotations.items():
            if annotations:
                base_name = os.path.basename(image_path)
                json_name = os.path.splitext(base_name)[0] + '.json'
                save_path = os.path.join(directory, json_name)

                data = {
                    'image_path': image_path,
                    'document_type': self.doc_type_combo.currentText(),
                    'image_size': {
                        'width': self.original_pixmap.width(),
                        'height': self.original_pixmap.height()
                    },
                    'annotations': annotations
                }
                
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)


    def export_by_format(self):
        """เลือกรูปแบบการ export ตามที่เลือกใน combo box"""
        # ตรวจสอบก่อน export
        is_valid, errors = self.validator.validate_annotations(
            self.annotations,
            self.doc_type_combo.currentText(),
            self.original_pixmap.height(),
            self.original_pixmap.width()
        )

        if not is_valid:
            error_text = "ไม่สามารถส่งออกได้เนื่องจากพบข้อผิดพลาด:\n\n"
            error_text += "\n".join([f"- {err}" for err in errors])
            QMessageBox.warning(self, "ไม่สามารถส่งออก", error_text)
            return

        selected_format = self.export_menu.currentText()
        
        directory = QFileDialog.getExistingDirectory(self, "เลือกโฟลเดอร์สำหรับบันทึก")
        if directory:
            # บันทึก annotations ปัจจุบันก่อน
            if self.image_path and self.annotations:
                self.save_current_annotations()
                # อัพเดท autosaver
                self.autosaver.update_current_data({
                    'image_path': self.image_path,
                    'document_type': self.doc_type_combo.currentText(),
                    'annotations': self.annotations,
                    'image_size': {
                        'width': self.original_pixmap.width(),
                        'height': self.original_pixmap.height()
                    }
                })
            
            if selected_format == "JSON ปกติ":
                self.export_annotations(directory)
            else:  # LayoutLM Format
                self.export_layoutlm_format(directory)

    def validate_current(self):
        """ตรวจสอบความถูกต้องของ annotations ปัจจุบัน"""
        if not self.annotations:
            QMessageBox.warning(self, "แจ้งเตือน", "ยังไม่มีการทำ annotation")
            return
            
        if not self.original_pixmap:
            QMessageBox.warning(self, "แจ้งเตือน", "ไม่พบรูปภาพ")
            return

        # เรียกใช้ validator
        is_valid, errors = self.validator.validate_annotations(
            self.annotations,
            self.doc_type_combo.currentText(),
            self.original_pixmap.height(),
            self.original_pixmap.width()
        )

        if is_valid:
            QMessageBox.information(
                self,
                "ผลการตรวจสอบ",
                "การ annotate ถูกต้องตามเงื่อนไขทั้งหมด"
            )
        else:
            error_text = "พบข้อผิดพลาด:\n\n"
            error_text += "\n".join([f"- {err}" for err in errors])
            QMessageBox.warning(self, "ข้อผิดพลาด", error_text)



def main():
    app = QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()