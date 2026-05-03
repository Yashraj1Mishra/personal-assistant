import sys
from PyQt6.QtWidgets import QApplication
from ui.splash import SplashWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Jarvis")
    splash = SplashWindow()
    splash.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 