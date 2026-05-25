import html

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
    QGridLayout,
)

from jarvis.core.memory import load_memory, save_memory
from jarvis.core.worker import CommandWorker
from jarvis.core.state import AppState
from jarvis.core.services.theme_services import ThemeService
from jarvis.core.services.training_services import TrainingService
from jarvis.ui.widgets.card_frame import CardFrame


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.setObjectName("MainWindow")
        self.resize(1280, 760)

        self.memory = load_memory()
        self.app_state = AppState()
        self.theme_service = ThemeService()
        self.training_service = TrainingService(self.memory)

        self.worker_thread = None
        self.worker = None
        self.pending_close_after_thread = False

        self.quick_action_map = {
            "Open YouTube": "open youtube",
            "Open Google": "open google",
            "Open GitHub": "open github",
            "Open Live News": "open live news",
            "What time is it?": "time",
            "Clear chat": "__clear_chat__",
            "Show training summary": "__training_summary__",
        }

        self.build_ui()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.theme_service.apply_window_theme(self)
        self.app_state.current_theme = self.theme_service.current_theme

        self.add_message("Jarvis", "Welcome back. I am online.", is_user=False)
        self.add_message(
            "Jarvis",
            "Use the sidebar to switch between chat, actions, training, and settings.",
            is_user=False,
        )

        self.refresh_summaries()
        self.update_send_button_state()
        self.update_training_button_state()
        self.input.setFocus()

    def build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)
        root.addWidget(self.build_sidebar(), 0)
        root.addWidget(self.build_content_area(), 1)

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(240)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        brand = QLabel("JARVIS")
        brand.setObjectName("BrandTitle")

        sub = QLabel("AI control portal")
        sub.setObjectName("BrandSubtitle")

        layout.addWidget(brand)
        layout.addWidget(sub)

        self.nav_chat = QPushButton("Chat")
        self.nav_actions = QPushButton("Actions")
        self.nav_training = QPushButton("Training")
        self.nav_settings = QPushButton("Settings")

        self.nav_buttons = [
            self.nav_chat,
            self.nav_actions,
            self.nav_training,
            self.nav_settings,
        ]

        for i, btn in enumerate(self.nav_buttons):
            btn.setCheckable(True)
            btn.setObjectName("NavButton")
            btn.clicked.connect(lambda checked, index=i: self.switch_page(index))
            layout.addWidget(btn)

        self.nav_chat.setChecked(True)
        layout.addStretch()

        self.sidebar_status = QLabel(self.app_state.sidebar_status)
        self.sidebar_status.setObjectName("SidebarStatus")
        layout.addWidget(self.sidebar_status)

        return sidebar

    def build_content_area(self):
        wrapper = QFrame()
        wrapper.setObjectName("ContentWrap")

        layout = QVBoxLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        header = QFrame()
        header.setObjectName("TopBar")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 14, 18, 14)

        self.page_title = QLabel(self.app_state.current_page)
        self.page_title.setObjectName("PageTitle")

        self.status = QLabel("Status: Online")
        self.status.setObjectName("StatusLabel")

        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.setObjectName("TopButton")
        self.theme_btn.clicked.connect(self.toggle_theme)

        header_layout.addWidget(self.page_title)
        header_layout.addStretch()
        header_layout.addWidget(self.status)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.theme_btn)

        self.stack = QStackedWidget()
        self.stack.setObjectName("PageStack")

        self.stack.addWidget(self.build_chat_page())
        self.stack.addWidget(self.build_actions_page())
        self.stack.addWidget(self.build_training_page())
        self.stack.addWidget(self.build_settings_page())

        layout.addWidget(header)
        layout.addWidget(self.stack, 1)

        return wrapper

    def build_chat_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        intro = CardFrame("Conversation")
        intro_text = QLabel("Type commands, ask questions, or route quick tasks through Jarvis.")
        intro_text.setWordWrap(True)
        intro_text.setObjectName("MutedLabel")
        intro.layout.addWidget(intro_text)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setObjectName("ChatArea")
        intro.layout.addWidget(self.chat)

        input_card = CardFrame("Command Input")
        bottom = QHBoxLayout()
        bottom.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command or ask a question...")
        self.input.setObjectName("InputBox")
        self.input.returnPressed.connect(self.send_command)
        self.input.textChanged.connect(self.update_send_button_state)

        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("PrimaryButton")
        self.send_btn.clicked.connect(self.send_command)
        self.send_btn.setEnabled(False)

        bottom.addWidget(self.input, 1)
        bottom.addWidget(self.send_btn)
        input_card.layout.addLayout(bottom)

        layout.addWidget(intro, 1)
        layout.addWidget(input_card, 0)

        return page

    def build_actions_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(14)

        top_card = CardFrame("Instant Actions")
        top_text = QLabel("These buttons run fast actions now, and later they can be reused for voice commands too.")
        top_text.setWordWrap(True)
        top_text.setObjectName("MutedLabel")
        top_card.layout.addWidget(top_text)

        grid_host = QWidget()
        grid = QGridLayout(grid_host)
        grid.setContentsMargins(0, 6, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        for index, label in enumerate(self.quick_action_map.keys()):
            btn = QPushButton(label)
            btn.setObjectName("ActionButton")
            btn.clicked.connect(lambda checked, text=label: self.run_quick_action(text))
            grid.addWidget(btn, index // 2, index % 2)

        top_card.layout.addWidget(grid_host)

        activity_card = CardFrame("Action Activity")
        self.action_log = QTextEdit()
        self.action_log.setReadOnly(True)
        self.action_log.setObjectName("LogArea")
        self.action_log.setPlainText("No actions executed yet.")
        activity_card.layout.addWidget(self.action_log)

        outer.addWidget(top_card)
        outer.addWidget(activity_card, 1)

        return page

    def build_training_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(14)

        train_card = CardFrame("Training Workspace")

        info = QLabel(
            "Use this area to define aliases, custom command mappings, and personal behavior rules for Jarvis."
        )
        info.setWordWrap(True)
        info.setObjectName("MutedLabel")
        train_card.layout.addWidget(info)

        self.training_input = QLineEdit()
        self.training_input.setPlaceholderText("Example note or alias idea...")
        self.training_input.setObjectName("InputBox")
        self.training_input.textChanged.connect(self.update_training_button_state)

        self.training_save_btn = QPushButton("Save Training Note")
        self.training_save_btn.setObjectName("PrimaryButton")
        self.training_save_btn.clicked.connect(self.save_training_note)
        self.training_save_btn.setEnabled(False)

        self.training_list = QListWidget()
        self.training_list.setObjectName("ListBox")

        for note in self.training_service.list_training_notes():
            self.training_list.addItem(str(note))

        train_card.layout.addWidget(self.training_input)
        train_card.layout.addWidget(self.training_save_btn)
        train_card.layout.addWidget(self.training_list)

        outer.addWidget(train_card, 1)
        return page

    def build_settings_page(self):
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(14)

        settings_card = CardFrame("Settings")

        self.theme_info = QLabel(f"Current theme: {self.theme_service.current_theme}")
        self.theme_info.setObjectName("MutedLabel")

        self.training_info = QLabel(self.training_service.get_summary())
        self.training_info.setWordWrap(True)
        self.training_info.setObjectName("MutedLabel")

        self.memory_info = QLabel(self.get_memory_summary())
        self.memory_info.setWordWrap(True)
        self.memory_info.setObjectName("MutedLabel")

        self.clear_chat_btn = QPushButton("Clear Chat")
        self.clear_chat_btn.setObjectName("SecondaryButton")
        self.clear_chat_btn.clicked.connect(self.clear_chat)

        self.refresh_memory_btn = QPushButton("Refresh Summary")
        self.refresh_memory_btn.setObjectName("SecondaryButton")
        self.refresh_memory_btn.clicked.connect(self.refresh_summaries)

        self.save_memory_btn = QPushButton("Save Memory Now")
        self.save_memory_btn.setObjectName("PrimaryButton")
        self.save_memory_btn.clicked.connect(self.persist_memory)

        settings_card.layout.addWidget(self.theme_info)
        settings_card.layout.addWidget(self.training_info)
        settings_card.layout.addWidget(self.memory_info)
        settings_card.layout.addWidget(self.clear_chat_btn)
        settings_card.layout.addWidget(self.refresh_memory_btn)
        settings_card.layout.addWidget(self.save_memory_btn)
        settings_card.layout.addStretch()

        outer.addWidget(settings_card, 1)
        return page

    def switch_page(self, index):
        page_names = ["Chat", "Actions", "Training", "Settings"]
        self.stack.setCurrentIndex(index)
        self.app_state.set_page(page_names[index])
        self.page_title.setText(self.app_state.current_page)

        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def update_send_button_state(self):
        can_send = bool(self.input.text().strip()) and not self.is_worker_busy()
        self.send_btn.setEnabled(can_send)

    def update_training_button_state(self):
        self.training_save_btn.setEnabled(bool(self.training_input.text().strip()))

    def add_message(self, sender, text, is_user=False):
        safe_sender = html.escape(str(sender))
        safe_text = html.escape(str(text)).replace("\n", "<br>")

        if self.theme_service.current_theme == "Neon":
            bubble_color = "#123d38" if is_user else "#101820"
            border_color = "#1fe0c3" if is_user else "#29434a"
            text_color = "#eafffb"
            sender_color = "#7fffd4"
        else:
            bubble_color = "#dff4ef" if is_user else "#f3f7fb"
            border_color = "#7ec9be" if is_user else "#cbd8e2"
            text_color = "#17313c"
            sender_color = "#17637c"

        align = "right" if is_user else "left"

        html_block = f"""
        <div style="margin: 10px 0; text-align: {align};">
            <div style="
                display: inline-block;
                max-width: 75%;
                background-color: {bubble_color};
                border: 1px solid {border_color};
                border-radius: 16px;
                padding: 12px 16px;
                color: {text_color};
                font-size: 15px;
            ">
                <div style="font-size: 11px; color: {sender_color}; margin-bottom: 4px; letter-spacing: 1px;">
                    {safe_sender}
                </div>
                <div>{safe_text}</div>
            </div>
        </div>
        """
        self.chat.append(html_block)
        scrollbar = self.chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def is_worker_busy(self):
        return self.worker_thread is not None and self.worker_thread.isRunning()

    def send_command(self):
        command = self.input.text().strip()
        if not command:
            return

        if self.is_worker_busy():
            self.status.setText("Status: Please wait, command still running")
            return

        self.app_state.remember_command(command)
        self.add_message("You", command, is_user=True)
        self.input.clear()
        self.set_busy_state(True)

        self.worker_thread = QThread()
        self.worker = CommandWorker(command, self.memory)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.on_command_finished)
        self.worker.error.connect(self.on_command_error)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)

        self.worker_thread.finished.connect(self.on_thread_finished)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def on_thread_finished(self):
        self.worker = None
        self.worker_thread = None

        if self.pending_close_after_thread:
            self.pending_close_after_thread = False
            self.close()

    def on_command_finished(self, result):
        if result not in ("exit", False, None):
            self.app_state.remember_result(str(result))
            self.add_message("Jarvis", str(result), is_user=False)

        self.refresh_summaries()
        self.set_busy_state(False)

        if result == "exit" or result is False:
            self.add_message("Jarvis", "Shutting down.", is_user=False)
            self.pending_close_after_thread = True

    def on_command_error(self, error_text):
        self.add_message("Jarvis", f"Something went wrong: {error_text}", is_user=False)
        self.status.setText("Status: Error")
        self.app_state.sidebar_status = "Last action failed"
        self.sidebar_status.setText(self.app_state.sidebar_status)
        self.set_busy_state(False)

    def set_busy_state(self, busy):
        self.app_state.set_busy(busy, "Processing command" if busy else "System stable")
        self.sidebar_status.setText(self.app_state.sidebar_status)

        if busy:
            self.status.setText("Status: Thinking...")
            self.send_btn.setEnabled(False)
            self.input.setEnabled(False)
            self.theme_btn.setEnabled(False)
        else:
            self.status.setText("Status: Online")
            self.input.setEnabled(True)
            self.theme_btn.setEnabled(True)
            self.input.setFocus()
            self.update_send_button_state()

    def run_quick_action(self, label):
        if self.is_worker_busy():
            self.status.setText("Status: Please wait, command still running")
            return

        command = self.quick_action_map.get(label, "")
        self.switch_page(0)

        if command == "__clear_chat__":
            self.clear_chat()
            self.log_action(f"{label} executed.")
            return

        if command == "__training_summary__":
            summary = self.training_service.get_summary()
            self.add_message("Jarvis", summary, is_user=False)
            self.log_action(f"{label} executed.")
            return

        self.input.setText(command)
        self.send_command()
        self.log_action(f"{label} executed.")

    def log_action(self, text):
        self.app_state.log(text)
        current = self.action_log.toPlainText().strip()
        if current == "No actions executed yet.":
            self.action_log.clear()
        self.action_log.append(text)

    def save_training_note(self):
        note = self.training_input.text().strip()
        ok, message = self.training_service.add_training_note(note)

        if not ok:
            self.status.setText(f"Status: {message}")
            return

        self.training_list.addItem(QListWidgetItem(note))
        self.training_input.clear()
        self.refresh_training_summary()
        self.update_training_button_state()
        self.status.setText(f"Status: {message}")
        self.app_state.sidebar_status = "Training updated"
        self.sidebar_status.setText(self.app_state.sidebar_status)

    def clear_chat(self):
        self.chat.clear()
        self.add_message("Jarvis", "Chat cleared. Ready for your next command.", is_user=False)
        self.status.setText("Status: Chat cleared")

    def persist_memory(self):
        save_memory(self.memory)
        self.refresh_summaries()
        self.status.setText("Status: Memory saved")
        self.app_state.sidebar_status = "Memory saved"
        self.sidebar_status.setText(self.app_state.sidebar_status)

    def refresh_training_summary(self):
        self.training_info.setText(self.training_service.get_summary())

    def refresh_summaries(self):
        self.refresh_training_summary()
        self.memory_info.setText(self.get_memory_summary())

    def get_memory_summary(self):
        memory_keys = ", ".join(sorted(self.memory.keys())) if self.memory else "no keys saved"
        return f"Memory keys: {memory_keys}"

    def toggle_theme(self):
        new_theme = self.theme_service.toggle_theme(self)
        self.app_state.current_theme = new_theme
        self.theme_info.setText(f"Current theme: {new_theme}")
        self.status.setText(f"Status: Theme changed to {new_theme}")
        self.sidebar_status.setText(self.app_state.sidebar_status)

    def cleanup_thread(self):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()

    def closeEvent(self, event: QCloseEvent):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.status.setText("Status: Stopping background task...")
            self.app_state.sidebar_status = "Stopping task"
            self.sidebar_status.setText(self.app_state.sidebar_status)
            self.cleanup_thread()

        event.accept()