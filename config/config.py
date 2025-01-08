from pathlib import Path

class Config:
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR.parent / 'data'
    
    # Data directories
    RAW_DIR = DATA_DIR / 'raw'
    ANNOTATIONS_DIR = DATA_DIR / 'annotations'
    TEMP_DIR = DATA_DIR / 'temp'
    
    # File patterns
    SUPPORTED_FORMATS = ['.pdf', '.jpg', '.jpeg', '.png']
    
    # Annotation settings
    MIN_BOX_SIZE = 20  # Minimum size for annotation box
    AUTOSAVE_INTERVAL = 5  # Minutes
    
    # Document types and their labels
    DOCUMENT_TYPES = {
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
        "หนังสือประทับตรา": {
            'ที่': '#FF0000',
            'ถึง': '#00FF00',
            'เรื่อง': '#0000FF',
            'ตราประทับ': '#FFFF00',
            'วันที่': '#FF00FF',
            'เนื้อความ': '#808080'
        }
    }

    @classmethod
    def ensure_directories(cls):
        """สร้าง directories ที่จำเป็น"""
        dirs = [cls.DATA_DIR, cls.RAW_DIR, 
                cls.ANNOTATIONS_DIR, cls.TEMP_DIR]
        for dir_path in dirs:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"[DEBUG] Config: Directory ensured: {dir_path}")
            except Exception as e:
                print(f"[ERROR] Config: Failed to create directory {dir_path}: {e}")
