from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal

from gui.shared import general_font

class HomePageNavigation(QWidget):

    universities_btn_clicked = Signal()
    subjects_btn_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.universities_btn = QPushButton("Университеты")
        self.universities_btn.setFixedWidth(150)
        self.universities_btn.setFont(general_font)
        self.universities_btn.clicked.connect(self.universities_btn_clicked)

        self.subjects_btn = QPushButton("Предметы")
        self.subjects_btn.setFixedWidth(150)
        self.subjects_btn.setFont(general_font)
        self.subjects_btn.clicked.connect(self.subjects_btn_clicked)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.universities_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.subjects_btn, 0, Qt.AlignmentFlag.AlignHCenter)