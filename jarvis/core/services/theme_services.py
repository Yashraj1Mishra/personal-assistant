from pathlib import Path


class ThemeService:
    def __init__(self, app=None):
        self.app = app
        self.current_theme = "Neon"

    def load_stylesheet(self, base_path: Path):
        qss_path = base_path / "jarvis" / "ui" / "theme.qss"
        if self.app and qss_path.exists():
            self.app.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def apply_window_theme(self, window):
        theme_value = "neon" if self.current_theme.lower() == "neon" else "slate"
        window.setProperty("theme", theme_value)
        window.style().unpolish(window)
        window.style().polish(window)
        window.update()

    def toggle_theme(self, window=None):
        self.current_theme = "Slate" if self.current_theme == "Neon" else "Neon"
        if window is not None:
            self.apply_window_theme(window)
        return self.current_theme