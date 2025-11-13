"""
Language creation workflow dialog.
Collects phonological, lexical, morphological, and grammatical preferences
before instantiating a LanguageProfile.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.language import (
    AffixDefinition,
    CustomStressPattern,
    DerivedWordDefinition,
    FootDirection,
    GrammarProfile,
    LanguageProfile,
    LexiconEntry,
    MainStressPosition,
    PartOfSpeech,
    PhonotacticProfile,
    StressPattern,
    StressSettings,
    WordOrder,
)


CONSONANT_PLACES = [
    "Bilabial",
    "Labiodental",
    "Dental",
    "Alveolar",
    "Postalveolar",
    "Retroflex",
    "Palatal",
    "Velar",
    "Uvular",
    "Pharyngeal",
    "Glottal",
]

PULMONIC_CONSONANTS: Dict[str, List[List[str]]] = {
    "Plosive": [
        ["p", "b"],
        ["p̪", "b̪"],
        ["t̪", "d̪"],
        ["t", "d"],
        [],
        ["ʈ", "ɖ"],
        ["c", "ɟ"],
        ["k", "ɡ"],
        ["q", "ɢ"],
        [],
        ["ʔ"],
    ],
    "Nasal": [
        ["m"],
        ["ɱ"],
        ["n̪"],
        ["n"],
        [],
        ["ɳ"],
        ["ɲ"],
        ["ŋ"],
        ["ɴ"],
        [],
        [],
    ],
    "Trill": [
        ["ʙ"],
        [],
        [],
        ["r"],
        [],
        [],
        [],
        [],
        ["ʀ"],
        [],
        [],
    ],
    "Tap or Flap": [
        [],
        ["ⱱ"],
        [],
        ["ɾ"],
        [],
        ["ɽ"],
        [],
        [],
        [],
        [],
        [],
    ],
    "Fricative": [
        ["ɸ", "β"],
        ["f", "v"],
        ["θ", "ð"],
        ["s", "z"],
        ["ʃ", "ʒ"],
        ["ʂ", "ʐ"],
        ["ç", "ʝ"],
        ["x", "ɣ"],
        ["χ", "ʁ"],
        ["ħ", "ʕ"],
        ["h", "ɦ"],
    ],
    "Lateral fricative": [
        [],
        [],
        [],
        ["ɬ", "ɮ"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ],
    "Approximant": [
        [],
        ["ʋ"],
        [],
        ["ɹ"],
        [],
        ["ɻ"],
        ["j"],
        ["ɰ"],
        [],
        [],
        [],
    ],
    "Lateral approximant": [
        [],
        [],
        [],
        ["l"],
        [],
        ["ɭ"],
        ["ʎ"],
        ["ʟ"],
        [],
        [],
        [],
    ],
}

NON_PULMONIC_CONSONANTS: Dict[str, List[str]] = {
    "Clicks": ["ʘ", "ǀ", "ǃ", "ǁ", "ǂ"],
    "Voiced implosives": ["ɓ", "ɗ", "ʄ", "ɠ", "ʛ"],
    "Ejectives": ["pʼ", "tʼ", "kʼ", "qʼ", "sʼ"],
}

OTHER_CONSONANT_SYMBOLS = [
    "ʍ",
    "w",
    "ɥ",
    "ʜ",
    "ʢ",
    "ʡ",
    "ɧ",
]

VOWEL_COLUMNS = ["Front", "Central", "Back"]

VOWEL_CHART: Dict[str, List[List[str]]] = {
    "Close": [["i", "y"], ["ɨ", "ʉ"], ["ɯ", "u"]],
    "Near-close": [["ɪ", "ʏ"], [], ["ʊ"]],
    "Close-mid": [["e", "ø"], ["ɘ", "ɵ"], ["ɤ", "o"]],
    "Mid": [[], ["ə", "ɚ"], []],
    "Open-mid": [["ɛ", "œ"], ["ɜ", "ɞ"], ["ʌ", "ɔ"]],
    "Near-open": [["æ"], ["ɐ"], []],
    "Open": [["a", "ɶ"], [], ["ɑ", "ɒ"]],
}

EXTRA_VOWELS = ["ɝ", "ɞ˞", "ᵻ", "ᵿ"]  # Rhotic and near vowels not in main grid


class IPAConsonantChart(QWidget):
    """Interactive IPA consonant chart with selectable symbols."""

    selection_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._checkboxes: Dict[str, QCheckBox] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        layout.addWidget(self._build_pulmonic_section())
        layout.addWidget(self._build_non_pulmonic_section())
        layout.addWidget(self._build_other_section())
        layout.addStretch()

    def _build_pulmonic_section(self) -> QWidget:
        container = QGroupBox("Pulmonic Consonants")
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(4)
        grid.setContentsMargins(8, 8, 8, 8)

        header = QLabel("")
        grid.addWidget(header, 0, 0)
        for col, place in enumerate(CONSONANT_PLACES, start=1):
            label = QLabel(place)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-weight: 600;")
            grid.addWidget(label, 0, col)

        for row, (manner, columns) in enumerate(PULMONIC_CONSONANTS.items(), start=1):
            row_label = QLabel(manner)
            row_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row_label.setStyleSheet("font-weight: 600;")
            grid.addWidget(row_label, row, 0)

            for col_index, symbols in enumerate(columns, start=1):
                cell_widget = QWidget()
                cell_layout = QVBoxLayout(cell_widget)
                cell_layout.setContentsMargins(4, 2, 4, 2)
                cell_layout.setSpacing(2)

                if symbols:
                    for symbol in symbols:
                        cell_layout.addWidget(self._make_checkbox(symbol))
                else:
                    placeholder = QLabel("")
                    cell_layout.addWidget(placeholder)

                grid.addWidget(cell_widget, row, col_index)

        group_layout = QVBoxLayout(container)
        group_layout.addWidget(grid_widget)
        return container

    def _build_non_pulmonic_section(self) -> QWidget:
        container = QGroupBox("Non-pulmonic Consonants")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        for category, symbols in NON_PULMONIC_CONSONANTS.items():
            group = QGroupBox(category)
            inner = QVBoxLayout(group)
            for symbol in symbols:
                inner.addWidget(self._make_checkbox(symbol))
            layout.addWidget(group)

        return container

    def _build_other_section(self) -> QWidget:
        container = QGroupBox("Other Symbols")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        for symbol in OTHER_CONSONANT_SYMBOLS:
            layout.addWidget(self._make_checkbox(symbol))

        return container

    def _make_checkbox(self, symbol: str) -> QCheckBox:
        checkbox = QCheckBox(symbol)
        checkbox.stateChanged.connect(lambda _state: self.selection_changed.emit())
        self._checkboxes[symbol] = checkbox
        return checkbox

    def selected_symbols(self) -> List[str]:
        return sorted(symbol for symbol, cb in self._checkboxes.items() if cb.isChecked())


class IPAVowelChart(QWidget):
    """Interactive IPA vowel chart with selectable symbols."""

    selection_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._checkboxes: Dict[str, QCheckBox] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        layout.addWidget(self._build_main_chart())
        layout.addWidget(self._build_extra_section())
        layout.addStretch()

    def _build_main_chart(self) -> QWidget:
        container = QGroupBox("Monophthongs")
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(4)
        grid.setContentsMargins(8, 8, 8, 8)

        header = QLabel("")
        grid.addWidget(header, 0, 0)
        for col, label in enumerate(VOWEL_COLUMNS, start=1):
            header_label = QLabel(label)
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_label.setStyleSheet("font-weight: 600;")
            grid.addWidget(header_label, 0, col)

        for row, (height, columns) in enumerate(VOWEL_CHART.items(), start=1):
            row_label = QLabel(height)
            row_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row_label.setStyleSheet("font-weight: 600;")
            grid.addWidget(row_label, row, 0)

            for col_index, symbols in enumerate(columns, start=1):
                cell_widget = QWidget()
                cell_layout = QVBoxLayout(cell_widget)
                cell_layout.setContentsMargins(4, 2, 4, 2)
                cell_layout.setSpacing(2)

                for symbol in symbols:
                    cell_layout.addWidget(self._make_checkbox(symbol))

                if not symbols:
                    cell_layout.addWidget(QLabel(""))

                grid.addWidget(cell_widget, row, col_index)

        group_layout = QVBoxLayout(container)
        group_layout.addWidget(grid_widget)
        return container

    def _build_extra_section(self) -> QWidget:
        container = QGroupBox("Additional Vowels")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        for symbol in EXTRA_VOWELS:
            layout.addWidget(self._make_checkbox(symbol))

        return container

    def _make_checkbox(self, symbol: str) -> QCheckBox:
        checkbox = QCheckBox(symbol)
        checkbox.stateChanged.connect(lambda _state: self.selection_changed.emit())
        self._checkboxes[symbol] = checkbox
        return checkbox

    def selected_symbols(self) -> List[str]:
        return sorted(symbol for symbol, cb in self._checkboxes.items() if cb.isChecked())


def _checked_items(widget: QListWidget) -> List[str]:
    values: List[str] = []
    for idx in range(widget.count()):
        item = widget.item(idx)
        if item.checkState() == Qt.CheckState.Checked:
            values.append(item.text())
    return values


class PhonologyPage(QWidget):
    """Collect phoneme inventory, phonotactics, and stress preferences."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(self._build_inventory_group())
        layout.addWidget(self._build_phonotactics_group())
        layout.addWidget(self._build_illegal_group())
        layout.addWidget(self._build_stress_group())
        layout.addStretch()

    def _build_inventory_group(self) -> QGroupBox:
        group = QGroupBox("Select Phoneme Inventory")
        grid_layout = QHBoxLayout(group)

        self.consonant_chart = IPAConsonantChart()
        self.vowel_chart = IPAVowelChart()

        grid_layout.addWidget(self.consonant_chart, stretch=2)
        grid_layout.addWidget(self.vowel_chart, stretch=1)

        hint_layout = QVBoxLayout()
        hint = QLabel(
            "Clusters are generated from the consonants you choose.\n"
            "You can then allow specific combinations in the section below."
        )
        hint.setWordWrap(True)
        hint_layout.addWidget(hint)
        hint_layout.addStretch()
        grid_layout.addLayout(hint_layout)

        # Update positional lists whenever base inventory changes
        self.consonant_chart.selection_changed.connect(self._on_inventory_changed)

        return group

    def _build_phonotactics_group(self) -> QGroupBox:
        group = QGroupBox("Allowed Consonant Positions")
        layout = QHBoxLayout(group)

        self.onset_list = QListWidget()
        self.onset_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.onset_list.setMinimumWidth(140)
        self.onset_list_label = QLabel("Word Onsets")

        self.medial_list = QListWidget()
        self.medial_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.medial_list.setMinimumWidth(140)
        self.medial_list_label = QLabel("Word Interior")

        self.coda_list = QListWidget()
        self.coda_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.coda_list.setMinimumWidth(140)
        self.coda_list_label = QLabel("Word Finals")

        onset_layout = QVBoxLayout()
        onset_layout.addWidget(self.onset_list_label)
        onset_layout.addWidget(self.onset_list)

        medial_layout = QVBoxLayout()
        medial_layout.addWidget(self.medial_list_label)
        medial_layout.addWidget(self.medial_list)

        coda_layout = QVBoxLayout()
        coda_layout.addWidget(self.coda_list_label)
        coda_layout.addWidget(self.coda_list)

        layout.addLayout(onset_layout)
        layout.addLayout(medial_layout)
        layout.addLayout(coda_layout)

        # Initialize with no options until inventory chosen
        self._update_position_lists()
        return group

    def _build_illegal_group(self) -> QGroupBox:
        group = QGroupBox("Illegal Combinations")
        layout = QVBoxLayout(group)
        prompt = QLabel(
            "List any disallowed consonant or vowel sequences.\n"
            "Enter one combination per line (e.g., 'ngw', 'aa')."
        )
        prompt.setWordWrap(True)
        self.illegal_text = QPlainTextEdit()
        self.illegal_text.setPlaceholderText("ngw\nbp\ntrr\n...")
        layout.addWidget(prompt)
        layout.addWidget(self.illegal_text)
        return group

    def _build_stress_group(self) -> QGroupBox:
        group = QGroupBox("Stress Pattern")
        layout = QVBoxLayout(group)

        self.stress_combo = QComboBox()
        for pattern in StressPattern:
            self.stress_combo.addItem(pattern.value, pattern)
        self.stress_combo.currentIndexChanged.connect(self._on_stress_changed)

        layout.addWidget(QLabel("Select the stress pattern that best fits your language:"))
        layout.addWidget(self.stress_combo)

        self.custom_widget = QWidget()
        form = QFormLayout(self.custom_widget)

        self.foot_size_combo = QComboBox()
        self.foot_size_combo.addItems(["2 syllables", "3 syllables"])
        self.foot_size_combo.currentIndexChanged.connect(self._sync_stress_syllable_choices)

        self.foot_direction_combo = QComboBox()
        self.foot_direction_combo.addItems(["Left to Right", "Right to Left"])

        self.stressed_syllable_combo = QComboBox()
        self.main_stress_combo = QComboBox()
        self.main_stress_combo.addItems(["Left-most foot", "Right-most foot"])

        form.addRow("Foot size:", self.foot_size_combo)
        form.addRow("Foot construction:", self.foot_direction_combo)
        form.addRow("Stress position inside foot:", self.stressed_syllable_combo)
        form.addRow("Main stress falls on:", self.main_stress_combo)

        layout.addWidget(self.custom_widget)
        self._sync_stress_syllable_choices()
        self._on_stress_changed()
        return group

    def _on_inventory_changed(self, _item: QListWidgetItem) -> None:
        self._update_position_lists()

    def _update_position_lists(self) -> None:
        consonants = self.consonant_chart.selected_symbols()
        clusters = self._generate_clusters(consonants)
        options = consonants + clusters

        self._rebuild_position_list(self.onset_list, options)
        self._rebuild_position_list(self.medial_list, options)
        self._rebuild_position_list(self.coda_list, options)

    def _rebuild_position_list(self, widget: QListWidget, options: List[str]) -> None:
        existing_states = {
            widget.item(index).text(): widget.item(index).checkState()
            for index in range(widget.count())
        }
        widget.blockSignals(True)
        widget.clear()
        for option in options:
            item = QListWidgetItem(option)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(existing_states.get(option, Qt.CheckState.Unchecked))
            widget.addItem(item)
        widget.blockSignals(False)

    def _generate_clusters(self, consonants: List[str]) -> List[str]:
        clusters = set()
        limit = 200
        for first in consonants:
            for second in consonants:
                if first == second:
                    continue
                clusters.add(first + second)
                if len(clusters) >= limit:
                    break
            if len(clusters) >= limit:
                break
        return sorted(clusters)

    def _sync_stress_syllable_choices(self) -> None:
        self.stressed_syllable_combo.clear()
        foot_size = 2 if self.foot_size_combo.currentIndex() == 0 else 3
        for idx in range(1, foot_size + 1):
            self.stressed_syllable_combo.addItem(f"{idx} syllable", idx)

    def _on_stress_changed(self) -> None:
        pattern = self.stress_combo.currentData()
        self.custom_widget.setVisible(pattern == StressPattern.CUSTOM_FOOT)

    def collect_data(self) -> tuple[PhonotacticProfile, StressSettings]:
        consonants = self.consonant_chart.selected_symbols()
        vowels = self.vowel_chart.selected_symbols()
        if not consonants:
            raise ValueError("Select at least one consonant for the language.")
        if not vowels:
            raise ValueError("Select at least one vowel for the language.")

        phonotactics = PhonotacticProfile(
            consonants=consonants,
            vowels=vowels,
            onset_clusters=_checked_items(self.onset_list),
            medial_clusters=_checked_items(self.medial_list),
            coda_clusters=_checked_items(self.coda_list),
            illegal_sequences=[
                line.strip()
                for line in self.illegal_text.toPlainText().splitlines()
                if line.strip()
            ],
        )

        pattern: StressPattern = self.stress_combo.currentData()
        custom = None
        if pattern == StressPattern.CUSTOM_FOOT:
            custom = CustomStressPattern(
                foot_size=2 if self.foot_size_combo.currentIndex() == 0 else 3,
                foot_direction=FootDirection.LEFT_TO_RIGHT
                if self.foot_direction_combo.currentIndex() == 0
                else FootDirection.RIGHT_TO_LEFT,
                stressed_syllable_in_foot=self.stressed_syllable_combo.currentData(),
                main_stress_position=(
                    MainStressPosition.LEFT_MOST
                    if self.main_stress_combo.currentIndex() == 0
                    else MainStressPosition.RIGHT_MOST
                ),
            )
            custom.validate()

        stress = StressSettings(pattern=pattern, custom_pattern=custom)
        return phonotactics, stress


class LexiconPage(QWidget):
    """Collect name and core lexicon entries."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        name_group = QGroupBox("Language Identity")
        name_layout = QFormLayout(name_group)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Leave blank to auto-generate a name")
        self.tagline_input = QLineEdit()
        self.tagline_input.setPlaceholderText("Optional motto or short description")
        name_layout.addRow("Language name:", self.name_input)
        name_layout.addRow("Tagline / description:", self.tagline_input)

        lexicon_group = QGroupBox("Seed Lexicon")
        lexicon_layout = QVBoxLayout(lexicon_group)
        instructions = QLabel(
            "Add any seed vocabulary. You can use either of the following formats per line:\n"
            "  • conlang_word : part-of-speech\n"
            "  • English word : part-of-speech = conlang word (IPA)\n"
            "Lines beginning with '#' are ignored."
        )
        instructions.setWordWrap(True)
        self.lexicon_edit = QPlainTextEdit()
        self.lexicon_edit.setPlaceholderText(
            "# Examples:\n"
            "vala : noun\n"
            "sunlight : noun = vala (ˈva.la)\n"
            "speak clearly : verb = reni lisa"
        )
        lexicon_layout.addWidget(instructions)
        lexicon_layout.addWidget(self.lexicon_edit)

        layout.addWidget(name_group)
        layout.addWidget(lexicon_group, stretch=1)
        layout.addStretch()

    def collect_data(self) -> tuple[Optional[str], List[LexiconEntry], str]:
        name = self.name_input.text().strip() or None
        tagline = self.tagline_input.text().strip()
        entries: List[LexiconEntry] = []
        for raw_line in self.lexicon_edit.toPlainText().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            english = ""
            conlang = ""
            ipa = ""
            part_of_speech = ""

            if "=" in line:
                left, right = [segment.strip() for segment in line.split("=", 1)]
                if ":" in left:
                    english, part_of_speech = [segment.strip() for segment in left.split(":", 1)]
                else:
                    english = left

                if "(" in right and ")" in right:
                    start = right.find("(")
                    end = right.rfind(")")
                    if end > start:
                        ipa = right[start + 1 : end].strip()
                        conlang = right[:start].strip()
                    else:
                        conlang = right
                else:
                    conlang = right
            else:
                if ":" in line:
                    conlang, part_of_speech = [segment.strip() for segment in line.split(":", 1)]
                else:
                    conlang = line

            entries.append(
                LexiconEntry(
                    conlang=conlang,
                    part_of_speech=part_of_speech,
                    english=english,
                    ipa=ipa,
                )
            )

        return name, entries, tagline


class MorphologyPage(QWidget):
    """Capture affixes and derived word information."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        affix_group = QGroupBox("Affixes")
        affix_layout = QVBoxLayout(affix_group)
        affix_instructions = QLabel(
            "List affixes in the format 'prefix/suffix/infix = description'. "
            "One per line. Lines starting with '#' are ignored."
        )
        affix_instructions.setWordWrap(True)
        self.affix_edit = QPlainTextEdit()
        self.affix_edit.setPlaceholderText(
            "# Example:\n"
            "-la = diminutive suffix\n"
            "ta- = agentive prefix"
        )
        affix_layout.addWidget(affix_instructions)
        affix_layout.addWidget(self.affix_edit)

        derived_group = QGroupBox("Derived Words")
        derived_layout = QVBoxLayout(derived_group)
        derived_instructions = QLabel(
            "Describe derived forms using 'base -> derived = gloss/notes'. "
            "For example: 'vala -> valaran = place of sunlight'."
        )
        derived_instructions.setWordWrap(True)
        self.derived_edit = QPlainTextEdit()
        self.derived_edit.setPlaceholderText(
            "vala -> valaran = place of sunlight\n"
            "reni -> reniala = proclamation"
        )
        derived_layout.addWidget(derived_instructions)
        derived_layout.addWidget(self.derived_edit)

        layout.addWidget(affix_group)
        layout.addWidget(derived_group, stretch=1)
        layout.addStretch()

    def collect_data(self) -> tuple[List[AffixDefinition], List[DerivedWordDefinition]]:
        affixes: List[AffixDefinition] = []
        for raw_line in self.affix_edit.toPlainText().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            label = line
            description = ""
            if "=" in line:
                label, description = [segment.strip() for segment in line.split("=", 1)]
            elif ":" in line:
                label, description = [segment.strip() for segment in line.split(":", 1)]

            affixes.append(AffixDefinition(label=label, description=description))

        derived: List[DerivedWordDefinition] = []
        for raw_line in self.derived_edit.toPlainText().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            base = ""
            derived_form = line
            gloss = ""

            if "->" in line:
                base_part, remainder = [segment.strip() for segment in line.split("->", 1)]
                base = base_part
                derived_form = remainder
            if "=" in derived_form:
                form_part, gloss = [segment.strip() for segment in derived_form.split("=", 1)]
                derived_form = form_part

            derived.append(DerivedWordDefinition(base=base or derived_form, derived_form=derived_form, gloss=gloss))

        return affixes, derived


class GrammarPage(QWidget):
    """Configure grammar preferences such as word order and optional POS."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        word_order_group = QGroupBox("Sentence Structure")
        word_order_layout = QFormLayout(word_order_group)
        self.word_order_combo = QComboBox()
        for order in WordOrder:
            self.word_order_combo.addItem(order.value, order)
        word_order_layout.addRow("Word order:", self.word_order_combo)

        optional_group = QGroupBox("Optional Parts of Speech")
        optional_layout = QVBoxLayout(optional_group)
        optional_instructions = QLabel(
            "Select any parts of speech that are optional or rare in your language."
        )
        optional_instructions.setWordWrap(True)
        self.optional_pos_list = QListWidget()
        self.optional_pos_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        for pos in PartOfSpeech:
            item = QListWidgetItem(pos.value)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.optional_pos_list.addItem(item)
        optional_layout.addWidget(optional_instructions)
        optional_layout.addWidget(self.optional_pos_list)

        notes_group = QGroupBox("Additional Notes")
        notes_layout = QVBoxLayout(notes_group)
        self.grammar_notes = QPlainTextEdit()
        self.grammar_notes.setPlaceholderText(
            "Document notable grammatical features, agreement systems, or exceptions."
        )
        notes_layout.addWidget(self.grammar_notes)

        layout.addWidget(word_order_group)
        layout.addWidget(optional_group)
        layout.addWidget(notes_group, stretch=1)
        layout.addStretch()

    def collect_data(self) -> GrammarProfile:
        order: WordOrder = self.word_order_combo.currentData()
        optional: List[PartOfSpeech] = []
        value_map: Dict[str, PartOfSpeech] = {entry.value: entry for entry in PartOfSpeech}
        for idx in range(self.optional_pos_list.count()):
            item = self.optional_pos_list.item(idx)
            if item.checkState() == Qt.CheckState.Checked:
                pos_enum = value_map.get(item.text())
                if pos_enum:
                    optional.append(pos_enum)

        return GrammarProfile(
            word_order=order,
            optional_parts_of_speech=optional,
            notes=self.grammar_notes.toPlainText().strip(),
        )


class LanguageCreationWizard(QDialog):
    """Dialog orchestrating the multi-step creation of a language profile."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Create New Language")
        self.resize(900, 720)

        self.phonology_page = PhonologyPage()
        self.lexicon_page = LexiconPage()
        self.morphology_page = MorphologyPage()
        self.grammar_page = GrammarPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.phonology_page)
        self.stack.addWidget(self.lexicon_page)
        self.stack.addWidget(self.morphology_page)
        self.stack.addWidget(self.grammar_page)

        self.button_box = QDialogButtonBox()
        self.back_button = self.button_box.addButton("Back", QDialogButtonBox.ButtonRole.ActionRole)
        self.next_button = self.button_box.addButton("Next", QDialogButtonBox.ButtonRole.ActionRole)
        self.finish_button = self.button_box.addButton("Finish", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_button = self.button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)

        self.back_button.clicked.connect(self._go_back)
        self.next_button.clicked.connect(self._go_next)
        self.finish_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout(self)
        header = QLabel(
            "Follow the steps to configure phonology, stress, vocabulary, and grammar for your language."
        )
        header.setWordWrap(True)
        header.setStyleSheet("font-size: 14px; font-weight: 500;")
        layout.addWidget(header)
        layout.addWidget(self.stack, stretch=1)
        layout.addWidget(self.button_box)

        self._language_profile: Optional[LanguageProfile] = None
        self._tagline: str = ""
        self._update_buttons()

    def _update_buttons(self) -> None:
        current_index = self.stack.currentIndex()
        page_count = self.stack.count()
        self.back_button.setEnabled(current_index > 0)
        if current_index == page_count - 1:
            self.next_button.setEnabled(False)
            self.finish_button.setEnabled(True)
        else:
            self.next_button.setEnabled(True)
            self.finish_button.setEnabled(False)

    def _go_back(self) -> None:
        index = self.stack.currentIndex()
        if index > 0:
            self.stack.setCurrentIndex(index - 1)
            self._update_buttons()

    def _go_next(self) -> None:
        index = self.stack.currentIndex()
        if index < self.stack.count() - 1:
            self.stack.setCurrentIndex(index + 1)
            self._update_buttons()

    def generate_language_name(self) -> str:
        prefixes = ["Ara", "Bel", "Cor", "Dra", "Eli", "Fara", "Gyl", "Hara", "Ith", "Jora"]
        suffixes = ["nion", "veth", "sira", "thar", "lune", "vash", "riel", "dora", "mora", "this"]
        middles = ["la", "ri", "ma", "ne", "sa", "lo", "na", "ro", "vi", "re"]
        return random.choice(prefixes) + random.choice(middles) + random.choice(suffixes)

    def accept(self) -> None:
        try:
            phonotactics, stress = self.phonology_page.collect_data()
            name, lexicon, tagline = self.lexicon_page.collect_data()
            affixes, derived = self.morphology_page.collect_data()
            grammar = self.grammar_page.collect_data()
        except ValueError as exc:
            QMessageBox.warning(self, "Incomplete Information", str(exc))
            return

        generated_name = None if name else self.generate_language_name()
        self._tagline = tagline
        self._language_profile = LanguageProfile.create(
            name=name,
            generated_name=generated_name,
            phonotactics=phonotactics,
            stress=stress,
            lexicon=lexicon,
            affixes=affixes,
            derived_words=derived,
            grammar=grammar,
        )
        super().accept()

    def get_language_profile(self) -> Optional[LanguageProfile]:
        return self._language_profile

    def get_tagline(self) -> str:
        return self._tagline
