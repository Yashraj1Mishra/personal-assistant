from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AppState:
    current_theme: str = "Neon"
    current_page: str = "Chat"
    is_busy: bool = False
    last_command: str = ""
    last_result: str = ""
    sidebar_status: str = "System stable"
    activity_log: List[str] = field(default_factory=list)
    session_data: Dict[str, Any] = field(default_factory=dict)

    def set_busy(self, value: bool, status: Optional[str] = None):
        self.is_busy = value
        if status:
            self.sidebar_status = status

    def set_page(self, page_name: str):
        self.current_page = page_name

    def remember_command(self, command: str):
        self.last_command = command

    def remember_result(self, result: str):
        self.last_result = result

    def log(self, message: str):
        self.activity_log.append(message)