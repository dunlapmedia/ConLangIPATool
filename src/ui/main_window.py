"""
Main application window coordinating the start workflow and primary tool tabs.
"""

from __future__ import annotations

from typing import Dict, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.language import LanguageProfile, StressPattern
from src.ui.language_creation import LanguageCreationWizard
from src.ui.start_screen import StartScreenWidget
from src.widgets import (
    DictionaryWidget,
    GrammarEditorWidget,
    IPAInputWidget,
    TranslatorWidget,
    TTSWidget,
)


class MainWindow(QMainWindow):
    """Main application window for ConLang IPA Tool."""

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config

        self.current_language: Optional[LanguageProfile] = None
        self.languages_store: Dict[str, LanguageProfile] = {}
        self.language_taglines: Dict[str, str] = {}

        self._init_ui()
        self.statusBar().showMessage("Select an option to get started.")

    def _init_ui(self) -> None:
        self.setWindowTitle("ConLang IPA Tool - Constructed Language Builder")
        self.setGeometry(100, 100, 1200, 820)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack)

        self.start_screen = StartScreenWidget()
        self.start_screen.create_language_requested.connect(self.launch_language_creation)
        self.start_screen.open_language_requested.connect(self.open_language)

        self.tabs = self._build_tab_widget()

        self.stack.addWidget(self.start_screen)
        self.stack.addWidget(self.tabs)
        self.stack.setCurrentWidget(self.start_screen)

        self._create_menu_bar()

    def _build_tab_widget(self) -> QTabWidget:
        tabs = QTabWidget()

        self.welcome_tab = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_tab)
        welcome_layout.setSpacing(16)
        welcome_layout.setContentsMargins(30, 30, 30, 30)

        self.welcome_title = QLabel("Welcome to ConLang IPA Tool")
        self.welcome_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_title.setStyleSheet("font-size: 26px; font-weight: bold;")

        self.welcome_tagline = QLabel(
            "Create a new language or open a previous project to begin."
        )
        self.welcome_tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_tagline.setWordWrap(True)
        self.welcome_tagline.setStyleSheet("font-size: 15px;")

        self.welcome_summary = QLabel("")
        self.welcome_summary.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.welcome_summary.setWordWrap(True)
        self.welcome_summary.setTextFormat(Qt.TextFormat.RichText)
        self.welcome_summary.setStyleSheet("font-size: 14px;")

        welcome_layout.addWidget(self.welcome_title)
        welcome_layout.addWidget(self.welcome_tagline)
        welcome_layout.addSpacing(20)
        welcome_layout.addWidget(self.welcome_summary)
        welcome_layout.addStretch()

        tabs.addTab(self.welcome_tab, "Overview")

        self.ipa_widget = IPAInputWidget()
        self.dictionary_widget = DictionaryWidget()
        self.grammar_widget = GrammarEditorWidget()
        self.translator_widget = TranslatorWidget()
        self.tts_widget = TTSWidget()

        tabs.addTab(self.ipa_widget, "IPA Input")
        tabs.addTab(self.dictionary_widget, "Dictionary")
        tabs.addTab(self.grammar_widget, "Grammar")
        tabs.addTab(self.translator_widget, "Translator")
        tabs.addTab(self.tts_widget, "TTS")

        return tabs

    def _create_menu_bar(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction("New Language", self)
        new_action.triggered.connect(self.launch_language_creation)
        file_menu.addAction(new_action)

        open_action = QAction("Open Language", self)
        open_action.triggered.connect(self.open_language)
        file_menu.addAction(open_action)

        save_action = QAction("Save Language", self)
        save_action.triggered.connect(self.save_language)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        return_start_action = QAction("Return to Start Screen", self)
        return_start_action.triggered.connect(self.return_to_start)
        file_menu.addAction(return_start_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def launch_language_creation(self) -> None:
        wizard = LanguageCreationWizard(self)
        if wizard.exec() == QDialog.DialogCode.Accepted:
            profile = wizard.get_language_profile()
            tagline = wizard.get_tagline()
            if profile:
                self.set_current_language(profile, tagline)
                self.statusBar().showMessage(f"Created language '{profile.display_name}'.")

    def set_current_language(self, profile: LanguageProfile, tagline: str = "") -> None:
        self.current_language = profile
        self.languages_store[profile.identifier] = profile
        if tagline:
            self.language_taglines[profile.identifier] = tagline

        self.stack.setCurrentWidget(self.tabs)
        self._update_welcome_tab(tagline)
        self._load_language_into_widgets(profile)

    def _load_language_into_widgets(self, profile: LanguageProfile) -> None:
        if hasattr(self.dictionary_widget, "load_from_language"):
            self.dictionary_widget.load_from_language(profile.lexicon)

        if hasattr(self.translator_widget, "load_lexicon"):
            self.translator_widget.load_lexicon(profile.lexicon)

        if hasattr(self.grammar_widget, "load_grammar_notes"):
            self.grammar_widget.load_grammar_notes(profile.grammar.notes or "")

    def _update_welcome_tab(self, tagline: str | None = None) -> None:
        if not self.current_language:
            self.welcome_title.setText("Welcome to ConLang IPA Tool")
            self.welcome_tagline.setText(
                "Create a new language or open a previous project to begin."
            )
            self.welcome_summary.clear()
            return

        profile = self.current_language
        summary_parts = []

        consonants = ", ".join(profile.phonotactics.consonants)
        vowels = ", ".join(profile.phonotactics.vowels)
        onsets = ", ".join(profile.phonotactics.onset_clusters)
        codas = ", ".join(profile.phonotactics.coda_clusters)

        summary_parts.append(
            "<b>Phoneme Inventory</b>"
            f"<ul>"
            f"<li>Consonants ({len(profile.phonotactics.consonants)}): {consonants}</li>"
            f"<li>Vowels ({len(profile.phonotactics.vowels)}): {vowels}</li>"
            f"<li>Word onsets: {onsets or 'No restrictions set'}</li>"
            f"<li>Word finals: {codas or 'No restrictions set'}</li>"
            "</ul>"
        )

        stress_label = profile.stress.pattern.value
        if profile.stress.pattern == StressPattern.CUSTOM_FOOT and profile.stress.custom_pattern:
            custom = profile.stress.custom_pattern
            stress_label = (
                f"Custom foot pattern — {custom.foot_size}-syllable feet built "
                f"from the {custom.foot_direction.value} edge with stress on syllable "
                f"{custom.stressed_syllable_in_foot}; main stress on the {custom.main_stress_position.value} foot."
            )
        summary_parts.append(f"<b>Stress Pattern</b><br>{stress_label}")

        summary_parts.append(
            "<b>Lexicon & Morphology</b>"
            f"<ul>"
            f"<li>Lexicon entries: {len(profile.lexicon)}</li>"
            f"<li>Affixes defined: {len(profile.affixes)}</li>"
            f"<li>Derived words: {len(profile.derived_words)}</li>"
            "</ul>"
        )

        summary_parts.append(
            "<b>Grammar</b>"
            f"<ul>"
            f"<li>Word order: {profile.grammar.word_order.value}</li>"
            f"<li>Optional parts of speech: "
            f"{', '.join(pos.value for pos in profile.grammar.optional_parts_of_speech) or 'None'}</li>"
            f"</ul>"
        )

        illegal_sequences = profile.phonotactics.illegal_sequences
        if illegal_sequences:
            summary_parts.append(
                "<b>Illegal Sequences</b><br>"
                + ", ".join(illegal_sequences)
            )

        self.welcome_title.setText(profile.display_name)
        if tagline:
            self.welcome_tagline.setText(tagline)
        else:
            stored_tagline = self.language_taglines.get(profile.identifier, "")
            self.welcome_tagline.setText(stored_tagline or "Custom constructed language overview.")

        self.welcome_summary.setText("<br><br>".join(summary_parts))

    def return_to_start(self) -> None:
        self.current_language = None
        self.stack.setCurrentWidget(self.start_screen)
        self._update_welcome_tab()
        self.statusBar().showMessage("Returned to start screen.")

    def open_language(self) -> None:
        if not self.languages_store:
            QMessageBox.information(
                self,
                "No Languages Found",
                "No languages have been created in this session yet.",
            )
            return

        dialog = LanguageSelectionDialog(
            list(self.languages_store.values()),
            self.language_taglines,
            self,
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            language_id = dialog.get_selected_language_id()
            if language_id and language_id in self.languages_store:
                self.set_current_language(
                    self.languages_store[language_id],
                    self.language_taglines.get(language_id, ""),
                )
                self.statusBar().showMessage(
                    f"Opened language '{self.languages_store[language_id].display_name}'."
                )

    def save_language(self) -> None:
        if not self.current_language:
            QMessageBox.information(self, "Nothing to Save", "Create or open a language first.")
            return
        QMessageBox.information(
            self,
            "Save Language",
            "Persistence is not yet implemented. Export options will be added in a future update.",
        )

    def show_about(self) -> None:
        QMessageBox.information(
            self,
            "About ConLang IPA Tool",
            "ConLang IPA Tool\n"
            "Version 1.0\n"
            "A Dunlap Media project for creating constructed languages with IPA support.",
        )


class LanguageSelectionDialog(QDialog):
    """Dialog for selecting a previously created language."""

    def __init__(
        self,
        languages: list[LanguageProfile],
        taglines: Dict[str, str],
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Open Language")
        self.resize(480, 360)

        self._selected_language_id: Optional[str] = None

        layout = QVBoxLayout(self)
        intro = QLabel("Choose a language to continue editing.")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self.list_widget = QListWidget()
        for profile in languages:
            item = QListWidgetItem(profile.display_name)
            item.setData(Qt.ItemDataRole.UserRole, profile.identifier)
            tagline = taglines.get(profile.identifier, "")
            if tagline:
                item.setToolTip(tagline)
            self.list_widget.addItem(item)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget, stretch=1)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Open | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        self._selected_language_id = item.data(Qt.ItemDataRole.UserRole)
        self.accept()

    def accept(self) -> None:
        current_item = self.list_widget.currentItem()
        if current_item:
            self._selected_language_id = current_item.data(Qt.ItemDataRole.UserRole)
            super().accept()
        else:
            QMessageBox.information(self, "Select a Language", "Please choose a language to open.")

    def get_selected_language_id(self) -> Optional[str]:
        return self._selected_language_id
