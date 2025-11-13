"""
IPA conversion helper widget.
Allows the user to experiment with simple orthography-to-IPA mappings.
"""

from __future__ import annotations

from typing import Dict, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
)


class IPAInputWidget(QWidget):
    """Widget offering a lightweight orthography to IPA converter."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._history: List[str] = []
        self._ipa_map = self._default_mapping()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("IPA Input Assistant")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        help_text = QLabel(
            "Enter orthographic text and generate an approximate IPA transcription. "
            "Mapping rules are intentionally simple and can be refined later."
        )
        help_text.setWordWrap(True)
        layout.addWidget(help_text)

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Type a word or phrase to convert…")
        self.input_edit.setMinimumHeight(100)
        layout.addWidget(self.input_edit)

        button_layout = QHBoxLayout()
        self.convert_button = QPushButton("Convert to IPA")
        self.convert_button.clicked.connect(self._on_convert_clicked)
        button_layout.addWidget(self.convert_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._clear_fields)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.output_edit = QTextEdit()
        self.output_edit.setPlaceholderText("IPA transcription will appear here…")
        self.output_edit.setReadOnly(True)
        self.output_edit.setMinimumHeight(80)
        layout.addWidget(self.output_edit)

        history_label = QLabel("Recent Conversions")
        history_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.itemActivated.connect(self._on_history_selected)
        layout.addWidget(self.history_list)

    def _default_mapping(self) -> Dict[str, str]:
        return {
            "a": "a",
            "e": "e",
            "i": "i",
            "o": "o",
            "u": "u",
            "y": "j",
            "c": "k",
            "q": "k",
            "x": "ks",
            "j": "ʒ",
            "g": "ɡ",
            "h": "h",
            "l": "l",
            "m": "m",
            "n": "n",
            "r": "ɾ",
            "s": "s",
            "z": "z",
            "t": "t",
            "d": "d",
            "p": "p",
            "b": "b",
            "f": "f",
            "v": "v",
            "k": "k",
            "w": "w",
        }

    def _on_convert_clicked(self) -> None:
        text = self.input_edit.toPlainText().strip()
        if not text:
            self.output_edit.setPlainText("")
            return

        ipa = self._to_ipa(text)
        self.output_edit.setPlainText(ipa)
        self._append_history(text, ipa)

    def _to_ipa(self, text: str) -> str:
        converted = []
        for char in text:
            ipa_value = self._ipa_map.get(char.lower(), char)
            # Preserve capitalization for the first character of words
            if char.isupper() and ipa_value:
                ipa_value = ipa_value.capitalize()
            converted.append(ipa_value)
        return "".join(converted)

    def _append_history(self, source: str, ipa: str) -> None:
        record = f"{source} → {ipa}"
        self._history.insert(0, record)
        self.history_list.insertItem(0, QListWidgetItem(record))
        if self.history_list.count() > 10:
            self.history_list.takeItem(self.history_list.count() - 1)

    def _clear_fields(self) -> None:
        self.input_edit.clear()
        self.output_edit.clear()

    def _on_history_selected(self, item: QListWidgetItem) -> None:
        self.output_edit.setPlainText(item.text().split("→", maxsplit=1)[-1].strip())
