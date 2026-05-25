from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from jarvis.core.agents.router import handle_flexible_command
from jarvis.core.memory import save_memory


class CommandWorker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, command, memory):
        super().__init__()
        self.command = command
        self.memory = memory

    @pyqtSlot()
    def run(self):
        try:
            result = handle_flexible_command(self.command, self.memory)
            save_memory(self.memory)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))