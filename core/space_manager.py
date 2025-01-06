# core/space_manager.py

class SpaceManager:
    """
    SpaceManager ทำหน้าที่จัดการการสื่อสารระหว่าง spaces
    และเป็นตัวกลางในการเข้าถึง spaces ต่างๆ
    """
    def __init__(self):
        # เก็บ instance ของแต่ละ space
        self._spaces = {}
        # เก็บ callback functions สำหรับแต่ละ event
        self._event_subscribers = {}

    def register_space(self, space_name: str, space_instance) -> None:
        """ลงทะเบียน space ใหม่"""
        self._spaces[space_name] = space_instance

    def get_space(self, space_name: str):
        """ดึง instance ของ space ที่ต้องการ"""
        return self._spaces.get(space_name)

    def subscribe_to_event(self, event_name: str, callback) -> None:
        """ลงทะเบียน callback function สำหรับ event"""
        if event_name not in self._event_subscribers:
            self._event_subscribers[event_name] = []
        self._event_subscribers[event_name].append(callback)

    def publish_event(self, event_name: str, data=None) -> None:
        """ส่ง event ไปยัง subscribers ทั้งหมด"""
        if event_name in self._event_subscribers:
            for callback in self._event_subscribers[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event handler for {event_name}: {str(e)}")