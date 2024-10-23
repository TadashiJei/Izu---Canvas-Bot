from canvasapi import Canvas
from typing import Optional

class UserObject:
    def __init__(self, token: Optional[str] = None):
        self._token = token
        self._API_URL = "https://csulb.instructure.com"
    
    def check_token(self) -> bool:
        if not self._token:
            return False
        canvas = Canvas(self._API_URL, self._token)
        try:
            user = canvas.get_current_user()
            return True
        except Exception:
            return False