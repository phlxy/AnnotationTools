class AnnotationValidator:
    def __init__(self, label_descriptions):
        self.label_descriptions = label_descriptions
        
    def validate_annotations(self, annotations, doc_type, image_height, image_width):
        """ตรวจสอบความถูกต้องของ annotations"""
        errors = []
        
        if not doc_type in self.label_descriptions:
            return False, ["ไม่พบประเภทเอกสารนี้"]
            
        # 1. ตรวจสอบฟิลด์ที่จำเป็น
        current_labels = {ann['label'] for ann in annotations}
        required_fields = set(self.label_descriptions[doc_type].keys())
        missing_fields = required_fields - current_labels
        
        if missing_fields:
            errors.append(f"ไม่พบฟิลด์ที่จำเป็น: {', '.join(missing_fields)}")

        # 2. ตรวจสอบตำแหน่ง y ของแต่ละฟิลด์ (เป็นเปอร์เซ็นต์)
        if doc_type == "หนังสือภายนอก":
            position_rules = {
                'ที่': {'max_y': 30},
                'ส่วนราชการ': {'max_y': 30},
                'วันที่': {'max_y': 30},
                'เรื่อง': {'min_y': 15, 'max_y': 40},
                'เรียน': {'min_y': 20, 'max_y': 50}
            }
        elif doc_type == "หนังสือภายใน":
            position_rules = {
                'ส่วนราชการ': {'max_y': 20},
                'ที่': {'max_y': 30},
                'วันที่': {'max_y': 30},
                'เรื่อง': {'min_y': 15, 'max_y': 40}
            }
        elif doc_type == "หนังสือประทับตรา":
            position_rules = {
                'ที่': {'max_y': 30},
                'ถึง': {'min_y': 15, 'max_y': 40},
                'ตราประทับ': {'max_y': 30}
            }

        for ann in annotations:
            label = ann['label']
            if label in position_rules:
                y_pos = (ann['coordinates']['y1'] / image_height) * 100
                rules = position_rules[label]
                
                if 'min_y' in rules and y_pos < rules['min_y']:
                    errors.append(f"{label}: อยู่สูงเกินไป ({y_pos:.1f}%)")
                if 'max_y' in rules and y_pos > rules['max_y']:
                    errors.append(f"{label}: อยู่ต่ำเกินไป ({y_pos:.1f}%)")

        # 3. ตรวจสอบการซ้ำซ้อนของฟิลด์
        label_counts = {}
        for ann in annotations:
            label = ann['label']
            label_counts[label] = label_counts.get(label, 0) + 1
            
            # ฟิลด์ที่ห้ามซ้ำ
            non_repeatable = ['ที่', 'วันที่', 'เรื่อง', 'เรียน', 'ส่วนราชการ']
            if label in non_repeatable and label_counts[label] > 1:
                errors.append(f"พบฟิลด์ {label} ซ้ำกัน {label_counts[label]} ครั้ง")

        # 4. ตรวจสอบการซ้อนทับ
        for i, ann1 in enumerate(annotations):
            for j, ann2 in enumerate(annotations[i+1:], i+1):
                overlap = self._calculate_overlap(ann1['coordinates'], ann2['coordinates'])
                if overlap > 50:  # ถ้าซ้อนทับเกิน 50%
                    errors.append(
                        f"พบการซ้อนทับระหว่าง {ann1['label']} และ {ann2['label']} ({overlap:.1f}%)"
                    )

        return len(errors) == 0, errors

    def _calculate_overlap(self, box1, box2):
        """คำนวณเปอร์เซ็นต์การซ้อนทับระหว่างสองกรอบ"""
        x_left = max(box1['x1'], box2['x1'])
        y_top = max(box1['y1'], box2['y1'])
        x_right = min(box1['x2'], box2['x2'])
        y_bottom = min(box1['y2'], box2['y2'])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection = (x_right - x_left) * (y_bottom - y_top)
        box1_area = (box1['x2'] - box1['x1']) * (box1['y2'] - box1['y1'])
        box2_area = (box2['x2'] - box2['x1']) * (box2['y2'] - box2['y1'])
        
        smaller_area = min(box1_area, box2_area)
        return (intersection / smaller_area) * 100