import sys
from PyQt6.QtWidgets import QApplication
from core.space_manager import SpaceManager
from spaces.ui_space.windows.main_window import MainWindow

def main():
    # สร้าง QApplication
    app = QApplication(sys.argv)
    
    # สร้าง Space Manager
    space_manager = SpaceManager()
    
    # สร้างหน้าต่างหลัก
    window = MainWindow(space_manager)
    window.show()
    
    # รัน application
    sys.exit(app.exec())

if __name__ == '__main__':
    main()