"""
Main Window for ConLang IPA Tool
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QLabel, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    """Main application window for ConLang IPA Tool"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ConLang IPA Tool - Constructed Language Builder")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Add placeholder tabs
        self.tabs.addTab(self.create_welcome_tab(), "Welcome")
        self.tabs.addTab(QLabel("IPA Input Widget\n(To be implemented)"), "IPA Input")
        self.tabs.addTab(QLabel("Dictionary Widget\n(To be implemented)"), "Dictionary")
        self.tabs.addTab(QLabel("Grammar Editor\n(To be implemented)"), "Grammar")
        self.tabs.addTab(QLabel("Translator Widget\n(To be implemented)"), "Translator")
        self.tabs.addTab(QLabel("Text-to-Speech Widget\n(To be implemented)"), "TTS")
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
    
    def create_welcome_tab(self):
        """Create the welcome tab"""
        welcome = QWidget()
        layout = QVBoxLayout(welcome)
        
        title = QLabel("Welcome to ConLang IPA Tool")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        
        description = QLabel(
            "A comprehensive constructed language building software\n"
            "with IPA support, grammar parsing, text-to-speech,\n"
            "and AI integration.\n\n"
            "Select a tab above to get started."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("font-size: 14px; margin: 20px;")
        
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        
        return welcome
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Language", self)
        new_action.triggered.connect(self.new_language)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Language", self)
        open_action.triggered.connect(self.open_language)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Language", self)
        save_action.triggered.connect(self.save_language)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def new_language(self):
        """Create a new language"""
        self.statusBar().showMessage("New Language (To be implemented)")
    
    def open_language(self):
        """Open an existing language"""
        self.statusBar().showMessage("Open Language (To be implemented)")
    
    def save_language(self):
        """Save the current language"""
        self.statusBar().showMessage("Save Language (To be implemented)")
    
    def show_about(self):
        """Show about dialog"""
        self.statusBar().showMessage("ConLang IPA Tool - Version 1.0 - By Dunlap Media")
