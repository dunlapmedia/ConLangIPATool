"""
Start screen for selecting between language creation and opening existing work.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StartScreenWidget(QWidget):
    """Landing screen that offers primary workflow choices."""

    create_language_requested = pyqtSignal()
    open_language_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("ConLang IPA Tool")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel(
            "Design phonology, build vocabularies, and guide grammar creation.\n"
            "Choose how you would like to begin."
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 14px;")

        create_button = QPushButton("Create New Language")
        create_button.setFixedWidth(220)
        create_button.clicked.connect(self.create_language_requested.emit)
        create_button.setStyleSheet("padding: 12px; font-size: 16px;")

        open_button = QPushButton("Open Existing Language")
        open_button.setFixedWidth(220)
        open_button.clicked.connect(self.open_language_requested.emit)
        open_button.setStyleSheet("padding: 12px; font-size: 16px;")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(create_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(open_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

