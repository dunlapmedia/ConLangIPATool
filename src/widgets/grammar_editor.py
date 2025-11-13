"""
Grammar editor widget providing a workspace for defining language rules.
"""

from __future__ import annotations

from typing import Dict, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPlainTextEdit,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QComboBox,
)


class GrammarEditorWidget(QWidget):
    """Lightweight grammar authoring surface."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.templates = self._default_templates()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("Grammar Editor")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title)

        description = QLabel(
            "Capture phonology, morphology, and syntax rules. "
            "Use templates to scaffold new sections and keep an outline for quick navigation."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(
            "# Phonology\n- Describe phoneme inventory...\n\n# Morphology\n- Document affixes…"
        )
        self.editor.textChanged.connect(self._update_outline)
        layout.addWidget(self.editor, stretch=3)

        template_layout = QHBoxLayout()
        self.template_selector = QComboBox()
        self.template_selector.addItems(self.templates.keys())
        template_layout.addWidget(QLabel("Insert Template:"))
        template_layout.addWidget(self.template_selector)

        insert_button = QPushButton("Insert")
        insert_button.clicked.connect(self._insert_template)
        template_layout.addWidget(insert_button)
        template_layout.addStretch()
        layout.addLayout(template_layout)

        outline_label = QLabel("Outline")
        outline_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(outline_label)

        self.outline = QListWidget()
        self.outline.itemActivated.connect(self._jump_to_section)
        layout.addWidget(self.outline, stretch=1)

        self._update_outline()

    def _default_templates(self) -> Dict[str, str]:
        return {
            "Phonology": "# Phonology\n- Consonants: \n- Vowels: \n- Phonotactics:\n",
            "Morphology": "# Morphology\n- Noun cases: \n- Verb conjugations: \n- Derivational patterns:\n",
            "Syntax": "# Syntax\n- Word order: \n- Clause structure: \n- Questions and negation:\n",
            "Semantics": "# Semantics\n- Key semantic domains: \n- Metaphors and idioms:\n",
        }

    def _insert_template(self) -> None:
        template_name = self.template_selector.currentText()
        template_text = self.templates.get(template_name, "")
        cursor = self.editor.textCursor()
        cursor.insertText(template_text + "\n")
        self.editor.setTextCursor(cursor)

    def _update_outline(self) -> None:
        self.outline.clear()
        headings = self._extract_headings(self.editor.toPlainText())
        for heading in headings:
            self.outline.addItem(QListWidgetItem(heading))

    def _extract_headings(self, text: str) -> List[str]:
        headings: List[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                headings.append(stripped.lstrip("# ").strip())
        return headings

    def _jump_to_section(self, item: QListWidgetItem) -> None:
        heading = item.text()
        block = self.editor.document().findBlockByLineNumber(0)
        cursor = self.editor.textCursor()
        while block.isValid():
            if block.text().lstrip("# ").strip() == heading:
                cursor.setPosition(block.position())
                self.editor.setTextCursor(cursor)
                self.editor.setFocus()
                return
            block = block.next()

    def load_grammar_notes(self, notes: str) -> None:
        """Populate the editor with existing grammar notes."""
        self.editor.setPlainText(notes)
        self._update_outline()
