"""
Translator widget providing a basic text translation workflow.
"""

from __future__ import annotations

import string
from typing import Dict, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

try:
    from src.core.language import LexiconEntry
except ImportError:  # pragma: no cover
    LexiconEntry = None  # type: ignore


class TranslatorWidget(QWidget):
    """Prototype translator interface using an in-memory lexicon."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._lexicon = self._default_lexicon()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Translator")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        instructions = QLabel(
            "Translate English input into your conlang using the working lexicon. "
            "Entries not found in the lexicon remain unchanged so you can expand them later."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        self.source_edit = QPlainTextEdit()
        self.source_edit.setPlaceholderText("Enter source text (e.g., 'The sunlight speaks clearly.')")
        self.source_edit.setMinimumHeight(120)
        layout.addWidget(self.source_edit)

        button_layout = QHBoxLayout()
        self.translate_button = QPushButton("Translate")
        self.translate_button.clicked.connect(self._translate)
        button_layout.addWidget(self.translate_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.output_edit = QPlainTextEdit()
        self.output_edit.setPlaceholderText("Translated output will appear here…")
        self.output_edit.setReadOnly(True)
        self.output_edit.setMinimumHeight(120)
        layout.addWidget(self.output_edit)

        lexicon_label = QLabel("Working Lexicon")
        lexicon_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(lexicon_label)

        self.lexicon_table = QTableWidget(0, 3)
        self.lexicon_table.setHorizontalHeaderLabels(["Source", "Target", "Notes"])
        header = self.lexicon_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.lexicon_table.verticalHeader().setVisible(False)
        self.lexicon_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.lexicon_table)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self._refresh_lexicon_table()

    def _default_lexicon(self) -> List[Dict[str, str]]:
        return [
            {"source": "sunlight", "target": "vala", "notes": "Matches dictionary entry"},
            {"source": "speak", "target": "reni", "notes": "Verb form; needs conjugation rules"},
            {"source": "clear", "target": "lisa", "notes": "Adjective meaning crisp/clear"},
            {"source": "the", "target": "sa", "notes": "Definite article placeholder"},
        ]

    def _refresh_lexicon_table(self) -> None:
        self.lexicon_table.setRowCount(len(self._lexicon))
        for row, entry in enumerate(self._lexicon):
            self.lexicon_table.setItem(row, 0, QTableWidgetItem(entry["source"]))
            self.lexicon_table.setItem(row, 1, QTableWidgetItem(entry["target"]))
            self.lexicon_table.setItem(row, 2, QTableWidgetItem(entry["notes"]))

    def _translate(self) -> None:
        source_text = self.source_edit.toPlainText().strip()
        if not source_text:
            self.status_label.setText("Enter text to translate.")
            self.output_edit.clear()
            return

        translation_map = {
            entry["source"].lower(): entry["target"]
            for entry in self._lexicon
            if entry.get("source")
        }
        translated_words: List[str] = []

        for token in source_text.split():
            translated_words.append(self._translate_token(token, translation_map))

        result = " ".join(translated_words)
        self.output_edit.setPlainText(result)
        self.status_label.setText("Translation complete.")

    def _translate_token(self, token: str, translation_map: Dict[str, str]) -> str:
        start = 0
        end = len(token)
        prefix = ""
        suffix = ""

        while start < end and token[start] in string.punctuation:
            prefix += token[start]
            start += 1
        while end > start and token[end - 1] in string.punctuation:
            suffix = token[end - 1] + suffix
            end -= 1

        core = token[start:end]
        if not core:
            return token

        translated_core = translation_map.get(core.lower(), core)

        if core[0].isupper():
            translated_core = translated_core.capitalize()

        return f"{prefix}{translated_core}{suffix}"

    def load_lexicon(self, lexicon_entries: List["LexiconEntry"]) -> None:  # type: ignore[name-defined]
        """Replace the working lexicon with data from a language profile."""
        if LexiconEntry is None:
            return

        self._lexicon = []
        for entry in lexicon_entries:
            source_display = entry.english or entry.conlang
            notes_components = [entry.part_of_speech]
            if entry.ipa:
                notes_components.append(entry.ipa)
            notes = ", ".join(filter(None, notes_components))
            self._lexicon.append(
                {"source": source_display, "target": entry.conlang, "notes": notes or "From profile"}
            )

        self._refresh_lexicon_table()
