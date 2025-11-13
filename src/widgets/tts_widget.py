"""
Text-to-Speech widget offering a preview/export stub.
"""

from __future__ import annotations

from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
)


class TTSWidget(QWidget):
    """Prototype TTS controller that stubs audio generation."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.voices = self._default_voices()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Text-to-Speech")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        description = QLabel(
            "Generate IPA-aware speech from phrases. "
            "This prototype keeps actions local and logs intended operations."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter IPA or romanized text to synthesize…")
        self.text_input.setMinimumHeight(120)
        layout.addWidget(self.text_input)

        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice:"))
        self.voice_selector = QComboBox()
        self.voice_selector.addItems(self.voices)
        voice_layout.addWidget(self.voice_selector)
        voice_layout.addStretch()
        layout.addLayout(voice_layout)

        button_layout = QHBoxLayout()
        self.preview_button = QPushButton("Preview")
        self.preview_button.clicked.connect(self._preview_audio)
        button_layout.addWidget(self.preview_button)

        self.export_button = QPushButton("Export Audio")
        self.export_button.clicked.connect(self._export_audio)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def _default_voices(self) -> List[str]:
        return ["Neutral", "Soft", "Resonant"]

    def _preview_audio(self) -> None:
        text = self.text_input.toPlainText().strip()
        if not text:
            self.status_label.setText("Enter text to preview.")
            return
        voice = self.voice_selector.currentText()
        self.status_label.setText(f"Previewing '{voice}' voice (simulation).")

    def _export_audio(self) -> None:
        text = self.text_input.toPlainText().strip()
        if not text:
            self.status_label.setText("Enter text before exporting.")
            return
        voice = self.voice_selector.currentText()
        self.status_label.setText(f"Prepared export with '{voice}' voice (simulation).")
