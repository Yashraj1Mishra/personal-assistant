from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen, QRadialGradient, QBrush
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
)

from ui.main_window import MainWindow


class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(40)

    def next_frame(self):
        self.frame += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w // 2
        cy = h // 2

        painter.fillRect(self.rect(), QColor("#05070a"))

        glow_radius = int(min(w, h) * 0.35)
        gradient = QRadialGradient(cx, cy, glow_radius)
        gradient.setColorAt(0.0, QColor(0, 255, 220, 35))
        gradient.setColorAt(0.4, QColor(0, 180, 160, 18))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - glow_radius, cy - glow_radius, glow_radius * 2, glow_radius * 2)

        for i in range(6):
            radius = 120 + i * 45 + ((self.frame + i * 12) % 45)
            alpha = max(25, 120 - i * 15)
            painter.setPen(QPen(QColor(79, 227, 193, alpha), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        if w > 0:
            for i in range(3):
                offset = int((self.frame * (i + 1) * 0.6) % w)
                painter.setPen(QPen(QColor(0, 255, 220, 25), 1))
                painter.drawLine(offset, 0, offset - 180, h)

        painter.setPen(QPen(QColor(0, 255, 220, 40), 1))
        painter.drawLine(cx - 320, cy, cx + 320, cy)
        painter.drawLine(cx, cy - 180, cx, cy + 180)

        painter.end()


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
        self.is_transitioning = False

        self.background = AnimatedBackground(self)
        self.background.lower()

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
                background: transparent;
            }
            QLabel#SplashTitle {
                color: #84ffe0;
                font-size: 76px;
                font-weight: 800;
                letter-spacing: 10px;
                background: transparent;
            }
            QLabel#SplashSubtitle {
                color: #b8c7d9;
                font-size: 20px;
                background: transparent;
            }
            QLabel#SplashStatus {
                color: #59f0d0;
                font-size: 16px;
                letter-spacing: 2px;
                background: transparent;
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

        self.auto_timer = QTimer(self)
        self.auto_timer.setSingleShot(True)
        self.auto_timer.timeout.connect(self.launch_main)
        self.auto_timer.start(4500)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.setGeometry(self.rect())

    def update_status(self):
        self.step_index = (self.step_index + 1) % len(self.status_steps)
        self.status.setText(self.status_steps[self.step_index])

    def launch_main(self):
       if self.is_transitioning:
        return

        self.is_transitioning = True
        self.timer.stop()
        self.auto_timer.stop()
        self.background.timer.stop()

        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(700)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_anim.finished.connect(self.open_main_window)
        self.fade_anim.start()

    def open_main_window(self):
        self.main = MainWindow()
        self.main.showFullScreen()
        self.close()