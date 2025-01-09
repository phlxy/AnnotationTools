import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QCheckBox, QScrollArea, QSplitter,
                            QFileDialog, QListWidget, QListWidgetItem)
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt6.QtCore import Qt, QRect

class ReviewerTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reviewer Interface")
        self.setGeometry(100, 100, 1600, 1000)
        
        # ตัวแปรสำหรับ zoom
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
        # ตัวแปรอื่นๆ
        self.image_path = None
        self.annotations = []
        self.original_pixmap = None
        self.visible_labels = {}
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(300)

        # ปุ่มโหลดไฟล์
        load_button = QPushButton("โหลดไฟล์ JSON")
        load_button.clicked.connect(self.load_json)
        left_layout.addWidget(load_button)

        # เพิ่มปุ่ม Zoom
        zoom_layout = QHBoxLayout()
        
        self.zoom_out_button = QPushButton("🔍-")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setFixedWidth(50)
        zoom_layout.addWidget(self.zoom_out_button)

        self.zoom_reset_button = QPushButton("100%")
        self.zoom_reset_button.clicked.connect(self.zoom_reset)
        self.zoom_reset_button.setFixedWidth(60)
        zoom_layout.addWidget(self.zoom_reset_button)

        self.zoom_in_button = QPushButton("🔍+")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setFixedWidth(50)
        zoom_layout.addWidget(self.zoom_in_button)
        
        left_layout.addLayout(zoom_layout)

        # Label Controls
        self.label_list = QListWidget()
        self.label_list.setMaximumHeight(200)
        left_layout.addWidget(QLabel("รายการ Labels:"))
        left_layout.addWidget(self.label_list)

        toggle_all = QPushButton("แสดง/ซ่อนทั้งหมด")
        toggle_all.clicked.connect(self.toggle_all_labels)
        left_layout.addWidget(toggle_all)

        left_layout.addStretch()
        layout.addWidget(left_panel)

        # Right Panel with Images
        right_panel = QSplitter(Qt.Orientation.Horizontal)
        
        # Original Image
        self.original_scroll = QScrollArea()
        self.original_scroll.setWidgetResizable(True)
        self.original_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_scroll.setWidget(self.original_image_label)
        
        # Annotated Image
        self.annotated_scroll = QScrollArea()
        self.annotated_scroll.setWidgetResizable(True)
        self.annotated_image_label = QLabel()
        self.annotated_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.annotated_scroll.setWidget(self.annotated_image_label)

        right_panel.addWidget(self.original_scroll)
        right_panel.addWidget(self.annotated_scroll)
        right_panel.setSizes([800, 800])
        
        layout.addWidget(right_panel)

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor = min(self.zoom_factor * 1.2, self.max_zoom)
            self.show_images()
            self.update_zoom_buttons()

    def zoom_out(self):
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor = max(self.zoom_factor * 0.8, self.min_zoom)
            self.show_images()
            self.update_zoom_buttons()

    def zoom_reset(self):
        self.zoom_factor = 1.0
        self.show_images()
        self.update_zoom_buttons()

    def update_zoom_buttons(self):
        self.zoom_out_button.setEnabled(self.zoom_factor > self.min_zoom)
        self.zoom_in_button.setEnabled(self.zoom_factor < self.max_zoom)
        self.zoom_reset_button.setText(f"{int(self.zoom_factor * 100)}%")

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

    def load_json(self):
        """โหลดไฟล์ JSON ที่มี annotations"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "เลือกไฟล์ JSON", "", "JSON Files (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # โหลดรูปภาพ
                self.image_path = data['image_path']
                image = QImage(self.image_path)
                self.original_pixmap = QPixmap.fromImage(image)

                # แปลงข้อมูลจาก LayoutLM format เป็น annotations
                if 'layout' in data:  # LayoutLM format
                    self.annotations = []
                    bbox_list = data['layout']['bbox']
                    label_list = data['layout']['label']
                    
                    for bbox, label in zip(bbox_list, label_list):
                        self.annotations.append({
                            'label': label,
                            'coordinates': {
                                'x1': bbox[0],
                                'y1': bbox[1],
                                'x2': bbox[2],
                                'y2': bbox[3]
                            }
                        })
                else:  # JSON ปกติ
                    self.annotations = data['annotations']
                
                # อัพเดท label list และ visibility
                self.update_label_list()
                
                # แสดงภาพ
                self.show_images()
                
            except Exception as e:
                print(f"Error loading JSON: {str(e)}")
                import traceback
                traceback.print_exc()  # แสดงรายละเอียดข้อผิดพลาด

    def update_label_list(self):
        """อัพเดทรายการ labels และสถานะการแสดง/ซ่อน"""
        self.label_list.clear()
        self.visible_labels.clear()
        
        # รวบรวม unique labels
        unique_labels = set(ann['label'] for ann in self.annotations)
        
        # เพิ่ม checkbox สำหรับแต่ละ label
        for label in unique_labels:
            checkbox = QCheckBox(label)
            checkbox.setChecked(True)
            self.visible_labels[label] = True
            
            # สร้าง widget item และใส่ checkbox
            item = QListWidgetItem()  # แก้จาก QListWidget.Item() เป็น QListWidgetItem()
            self.label_list.addItem(item)
            self.label_list.setItemWidget(item, checkbox)
            
            # เชื่อมต่อ signal
            checkbox.stateChanged.connect(self.show_images)

    def toggle_all_labels(self):
        """สลับการแสดง/ซ่อนทั้งหมด"""
        # ตรวจสอบว่ามี label ที่ซ่อนอยู่หรือไม่
        any_hidden = any(not v for v in self.visible_labels.values())
        
        # ถ้ามี label ที่ซ่อนอยู่ ให้แสดงทั้งหมด ถ้าไม่มีให้ซ่อนทั้งหมด
        new_state = Qt.CheckState.Checked if any_hidden else Qt.CheckState.Unchecked
        
        # อัพเดททุก checkbox
        for i in range(self.label_list.count()):
            item = self.label_list.item(i)
            checkbox = self.label_list.itemWidget(item)
            checkbox.setChecked(new_state == Qt.CheckState.Checked)
        
        self.show_images()

    def show_images(self):
        if not self.original_pixmap:
            return
            
        # คำนวณขนาดที่ต้องการหลัง zoom
        scaled_width = int(self.original_pixmap.width() * self.zoom_factor)
        scaled_height = int(self.original_pixmap.height() * self.zoom_factor)

        # แสดงภาพต้นฉบับ
        scaled_original = self.original_pixmap.scaled(
            scaled_width,
            scaled_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.original_image_label.setPixmap(scaled_original)
        
        # สร้างภาพที่มี annotations
        annotated_pixmap = self.original_pixmap.copy()
        painter = QPainter(annotated_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # อัพเดท visible_labels จาก checkboxes
        for i in range(self.label_list.count()):
            item = self.label_list.item(i)
            checkbox = self.label_list.itemWidget(item)
            self.visible_labels[checkbox.text()] = checkbox.isChecked()
        
        # วาด annotations ที่เลือกแสดง
        for ann in self.annotations:
            if self.visible_labels.get(ann['label'], True):
                color = QColor("#FF0000")  # ควรกำหนดสีตาม label
                painter.setPen(QPen(color, 3, Qt.PenStyle.SolidLine))
                
                coords = ann['coordinates']
                painter.drawRect(
                    coords['x1'],
                    coords['y1'],
                    coords['x2'] - coords['x1'],
                    coords['y2'] - coords['y1']
                )
                
                font = painter.font()
                font.setPointSize(10)
                painter.setFont(font)
                
                # วาดพื้นหลังสำหรับ label
                text_rect = painter.fontMetrics().boundingRect(ann['label'])
                bg_rect = QRect(
                    coords['x1'],
                    coords['y1'] - text_rect.height(),
                    text_rect.width() + 10,
                    text_rect.height()
                )
                painter.fillRect(bg_rect, QColor(255, 255, 255, 200))
                
                # วาด label
                painter.drawText(
                    coords['x1'] + 5,
                    coords['y1'] - 5,
                    ann['label']
                )
        
        painter.end()
        
        # แสดงภาพที่มี annotations
        scaled_annotated = annotated_pixmap.scaled(
            scaled_width,
            scaled_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.annotated_image_label.setPixmap(scaled_annotated)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReviewerTool()
    window.show()
    sys.exit(app.exec())