from pdf2image import convert_from_path
import os
import shutil

class DocumentLoader:
    def __init__(self, temp_dir="temp_images"):
        self.temp_dir = temp_dir
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
    def load_document(self, file_path):
        """โหลดเอกสาร รองรับทั้ง PDF และรูปภาพ"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.load_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            return self.load_image(file_path)
        else:
            raise ValueError("ไม่รองรับไฟล์ประเภทนี้")

    def load_pdf(self, pdf_path):
        """แปลง PDF เป็นรูปภาพ"""
        basename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.join(self.temp_dir, basename)
        
        # ลบโฟลเดอร์เก่าถ้ามี
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        
        # แปลง PDF เป็นรูปภาพ
        pages = convert_from_path(pdf_path)
        image_paths = []
        
        for i, page in enumerate(pages):
            image_path = os.path.join(output_dir, f"page_{i+1}.jpg")
            page.save(image_path, "JPEG")
            image_paths.append({
                'path': image_path,
                'page': i+1,
                'type': 'pdf_page',
                'original_path': pdf_path
            })
            
        return image_paths

    def load_image(self, image_path):
        """จัดการไฟล์รูปภาพ"""
        return [{
            'path': image_path,
            'page': 1,
            'type': 'image',
            'original_path': image_path
        }]

    def cleanup(self):
        """ลบไฟล์ชั่วคราวทั้งหมด"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)