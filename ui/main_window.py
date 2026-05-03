import io
from contextlib import redirect_stdout

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from jarvis.router import handle_flexible_command
from jarvis.memory import load_memory, save_memory


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.setObjectName("MainWindow")
        self.memory = load_memory()

        self.title = QLabel("JARVIS ONLINE")
        self.title.setObjectName("MainTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status = QLabel("Status: Online")
        self.status.setObjectName("StatusLabel")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setObjectName("ChatArea")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command or ask a question...")
        self.input.setObjectName("InputBox")
        self.input.returnPressed.connect(self.send_command)

        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("SendButton")
        self.send_btn.clicked.connect(self.send_command)

        bottom = QHBoxLayout()
        bottom.addWidget(self.input)
        bottom.addWidget(self.send_btn)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(14)
        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.chat)
        layout.addLayout(bottom)

        self.setStyleSheet("""
            QWidget#MainWindow {
                background: #05070a;
            }
            QLabel#MainTitle {
                color: #7fffd4;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: 4px;
            }
            QLabel#StatusLabel {
                color: #59f0d0;
                font-size: 14px;
                letter-spacing: 2px;
            }
            QTextEdit#ChatArea {
                background: rgba(10, 14, 18, 0.94);
                color: #dffdf7;
                border: 1px solid rgba(127, 255, 212, 0.18);
                border-radius: 18px;
                padding: 14px;
                font-size: 15px;
            }
            QLineEdit#InputBox {
                background: rgba(12, 16, 20, 0.96);
                color: #e8fff9;
                border: 1px solid rgba(127, 255, 212, 0.25);
                border-radius: 16px;
                padding: 14px 16px;
                font-size: 16px;
            }
            QPushButton#SendButton {
                background: rgba(0, 255, 220, 0.16);
                color: #eafffb;
                border: 1px solid rgba(127, 255, 212, 0.35);
                border-radius: 16px;
                padding: 14px 26px;
                font-size: 16px;
            }
            QPushButton#SendButton:hover {
                background: rgba(0, 255, 220, 0.26);
            }
        """)

        self.add_message("Jarvis", "Welcome back. I am online.", is_user=False)
        self.add_message("Jarvis", "Type a command or ask me anything.", is_user=False)
        self.input.setFocus()

    def add_message(self, sender, text, is_user=False):
        bubble_color = "#123d38" if is_user else "#101820"
        border_color = "#1fe0c3" if is_user else "#29434a"
        align = "right" if is_user else "left"

        html = f"""
        <div style="margin: 10px 0; text-align: {align};">
            <div style="
                display: inline-block;
                max-width: 75%;
                background-color: {bubble_color};
                border: 1px solid {border_color};
                border-radius: 16px;
                padding: 12px 16px;
                color: #eafffb;
                font-size: 15px;
            ">
                <div style="font-size: 11px; color: #7fffd4; margin-bottom: 4px; letter-spacing: 1px;">
                    {sender}
                </div>
                <div>{text}</div>
            </div>
        </div>
        """
        self.chat.append(html)
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())

    def send_command(self):
        command = self.input.text().strip()
        if not command:
            return

        self.add_message("You", command, is_user=True)
        self.input.clear()
        self.status.setText("Status: Thinking...")

        captured_output = io.StringIO()

        try:
            with redirect_stdout(captured_output):
                result = handle_flexible_command(command, self.memory)

            output_text = captured_output.getvalue().strip()

            if output_text:
                for line in output_text.splitlines():
                    self.add_message("Jarvis", line, is_user=False)

            save_memory(self.memory)
            self.status.setText("Status: Online")

            if result == "exit" or result is False:
                self.add_message("Jarvis", "Shutting down.", is_user=False)
                self.close()

        except Exception as e:
            self.add_message("Jarvis", f"Something went wrong: {e}", is_user=False)
            self.status.setText("Status: Error")