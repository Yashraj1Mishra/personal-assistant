from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)

from jarvis.ui.main_window import MainWindow


class PulseLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._glow = 0.25

    def getGlow(self):
        return self._glow

    def setGlow(self, value):
        self._glow = value
        self.update()

    glow = pyqtProperty(float, fget=getGlow, fset=setGlow)

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(12, 0, -12, 0)
        alpha = int(255 * self._glow)
        painter.setPen(QPen(QColor(79, 227, 193, alpha), 3))
        painter.drawLine(rect.left(), rect.center().y(), rect.right(), rect.center().y())

        painter.end()


class SplashWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis")
        self.setObjectName("SplashWindow")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.is_transitioning = False
        self.main = None

        self.title = QLabel("JARVIS")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("SplashTitle")

        self.subtitle = QLabel("Your futuristic AI assistant is initializing...")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setObjectName("SplashSubtitle")

        self.status = QLabel("Booting core systems")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setObjectName("SplashStatus")

        self.progress = PulseLine()
        self.progress.setFixedHeight(12)

        self.start_btn = QPushButton("Start Jarvis")
        self.start_btn.setObjectName("StartButton")
        self.start_btn.clicked.connect(self.launch_main)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 80, 80, 80)
        layout.setSpacing(18)
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.status)
        layout.addWidget(self.progress)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setStyleSheet("""
            QWidget#SplashWindow {
                background-color: #05070a;
            }
            QLabel#SplashTitle {
                color: #84ffe0;
                font-size: 76px;
                font-weight: 800;
                letter-spacing: 10px;
            }
            QLabel#SplashSubtitle {
                color: #b8c7d9;
                font-size: 20px;
            }
            QLabel#SplashStatus {
                color: #59f0d0;
                font-size: 16px;
                letter-spacing: 2px;
            }
            QPushButton#StartButton {
                background: rgba(0, 255, 220, 0.12);
                color: #eafffb;
                border: 1px solid rgba(132, 255, 224, 0.45);
                border-radius: 18px;
                padding: 14px 28px;
                font-size: 18px;
            }
            QPushButton#StartButton:hover {
                background: rgba(0, 255, 220, 0.22);
            }
            QPushButton#StartButton:pressed {
                background: rgba(0, 255, 220, 0.30);
            }
        """)

        shadow = QGraphicsDropShadowEffect(self.title)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 255, 220, 180))
        shadow.setOffset(0, 0)
        self.title.setGraphicsEffect(shadow)

        self.title_anim = QPropertyAnimation(shadow, b"blurRadius")
        self.title_anim.setStartValue(24)
        self.title_anim.setEndValue(60)
        self.title_anim.setDuration(1600)
        self.title_anim.setLoopCount(-1)
        self.title_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.title_anim.start()

        self.progress_anim = QPropertyAnimation(self.progress, b"glow")
        self.progress_anim.setStartValue(0.2)
        self.progress_anim.setEndValue(1.0)
        self.progress_anim.setDuration(900)
        self.progress_anim.setLoopCount(-1)
        self.progress_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.progress_anim.start()

        self.status_steps = [
            "Booting core systems",
            "Loading neural matrix",
            "Connecting AI interface",
            "Preparing command channel",
        ]
        self.step_index = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(900)

    def update_status(self):
        self.step_index = (self.step_index + 1) % len(self.status_steps)
        self.status.setText(self.status_steps[self.step_index])

    def launch_main(self):
        if self.is_transitioning:
            return

        self.is_transitioning = True
        self.timer.stop()
        self.title_anim.stop()
        self.progress_anim.stop()

        self.main = MainWindow()
        self.main.show()

        self.close()