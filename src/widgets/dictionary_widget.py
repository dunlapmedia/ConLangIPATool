"""
Dictionary management widget for the ConLang IPA Tool.
Provides a simple interface for adding, searching, and reviewing lexicon entries.
"""

from __future__ import annotations

from typing import Dict, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QComboBox,
    QTextEdit,
)

try:
    from src.core.language import LexiconEntry, PartOfSpeech
except ImportError:  # pragma: no cover
    PartOfSpeech = None  # type: ignore
    LexiconEntry = None  # type: ignore


class DictionaryWidget(QWidget):
    """Simple in-memory lexicon manager."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._entries: List[Dict[str, str]] = []
        self._init_ui()
        self._load_sample_entries()
        self._refresh_table(self._entries)

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Dictionary")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search lexicon…")
        self.search_input.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table of entries
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Word", "IPA", "Part of Speech", "Definition"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        # Entry form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(4)

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Word form (e.g., 'vala')")
        form_layout.addWidget(QLabel("Word:"))
        form_layout.addWidget(self.word_input)

        self.ipa_input = QLineEdit()
        self.ipa_input.setPlaceholderText("IPA transcription (e.g., /ˈva.la/)")
        form_layout.addWidget(QLabel("IPA:"))
        form_layout.addWidget(self.ipa_input)

        self.pos_input = QComboBox()
        self.pos_input.setEditable(False)
        self.pos_input.addItems(self._part_of_speech_options())
        form_layout.addWidget(QLabel("Part of Speech:"))
        form_layout.addWidget(self.pos_input)

        self.definition_input = QTextEdit()
        self.definition_input.setPlaceholderText("Short definition or usage notes…")
        self.definition_input.setFixedHeight(70)
        form_layout.addWidget(QLabel("Definition:"))
        form_layout.addWidget(self.definition_input)

        layout.addLayout(form_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.add_button = QPushButton("Add Entry")
        self.add_button.clicked.connect(self._add_entry)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self._remove_selected)
        button_layout.addWidget(self.remove_button)

        layout.addLayout(button_layout)

    def _part_of_speech_options(self) -> List[str]:
        if PartOfSpeech:
            return [item.value for item in PartOfSpeech]
        return [
            "noun",
            "verb",
            "adjective",
            "adverb",
            "pronoun",
            "preposition",
            "conjunction",
            "interjection",
        ]

    def _load_sample_entries(self) -> None:
        self._entries.extend(
            [
                {
                    "word": "vala",
                    "ipa": "ˈva.la",
                    "pos": "noun",
                    "definition": "sunlight; literal light from the sky",
                },
                {
                    "word": "reni",
                    "ipa": "ˈre.ni",
                    "pos": "verb",
                    "definition": "to speak with emphasis; to proclaim",
                },
            ]
        )

    def _refresh_table(self, entries: List[Dict[str, str]]) -> None:
        self.table.setRowCount(len(entries))
        for row, entry in enumerate(entries):
            self.table.setItem(row, 0, QTableWidgetItem(entry["word"]))
            self.table.setItem(row, 1, QTableWidgetItem(entry["ipa"]))
            self.table.setItem(row, 2, QTableWidgetItem(entry["pos"]))
            self.table.setItem(row, 3, QTableWidgetItem(entry["definition"]))

    def _on_search_changed(self, text: str) -> None:
        text = text.strip().lower()
        if not text:
            self._refresh_table(self._entries)
            return

        filtered = [
            entry
            for entry in self._entries
            if text in entry["word"].lower() or text in entry["definition"].lower()
        ]
        self._refresh_table(filtered)

    def _add_entry(self) -> None:
        word = self.word_input.text().strip()
        ipa = self.ipa_input.text().strip()
        pos = self.pos_input.currentText().strip()
        definition = self.definition_input.toPlainText().strip()

        if not word or not ipa or not definition:
            QMessageBox.warning(self, "Missing Information", "Please complete all fields.")
            return

        if any(entry["word"].lower() == word.lower() for entry in self._entries):
            QMessageBox.information(self, "Duplicate Entry", f"'{word}' already exists in the lexicon.")
            return

        entry = {"word": word, "ipa": ipa, "pos": pos, "definition": definition}
        self._entries.append(entry)
        self._refresh_table(self._entries)
        self.word_input.clear()
        self.ipa_input.clear()
        self.definition_input.clear()
        self.pos_input.setCurrentIndex(0)

    def _remove_selected(self) -> None:
        selected_rows = {index.row() for index in self.table.selectedIndexes()}
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Select a row to remove.")
            return

        for row in sorted(selected_rows, reverse=True):
            if 0 <= row < len(self._entries):
                del self._entries[row]

        self._refresh_table(self._entries)

    def load_from_language(self, lexicon_entries: List["LexiconEntry"]) -> None:  # type: ignore[name-defined]
        """Populate the dictionary table from a language profile."""
        if LexiconEntry is None:
            return

        self._entries = [
            {
                "word": entry.conlang,
                "ipa": entry.ipa,
                "pos": entry.part_of_speech,
                "definition": entry.english,
            }
            for entry in lexicon_entries
        ]
        self._refresh_table(self._entries)
