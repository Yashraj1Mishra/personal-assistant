from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel


class CardFrame(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("Card")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(12)

        if title:
            header = QLabel(title)
            header.setObjectName("CardTitle")
            self.layout.addWidget(header)