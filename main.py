import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from jarvis.ui.splash import SplashWindow


def load_stylesheet(app):
    base_dir = Path(__file__).resolve().parent
    qss_path = base_dir / "jarvis" / "ui" / "theme.qss"

    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        print(f"Stylesheet not found: {qss_path}")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Jarvis")

    load_stylesheet(app)

    splash = SplashWindow()
    splash.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()