"""
ConLang IPA Tool - Main Application Entry Point
A comprehensive constructed language building software with IPA support,
grammar parsing, text-to-speech, and AI integration.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.ui.main_window import MainWindow
from src.core.config import Config
from src.core.logger import setup_logger

def main():
    """Initialize and run the ConLang IPA Tool application."""
    # Set up logging
    logger = setup_logger()
    logger.info("Starting ConLang IPA Tool")
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Set up application
    app = QApplication(sys.argv)
    app.setApplicationName("ConLang IPA Tool")
    app.setOrganizationName("Dunlap Media")
    app.setApplicationDisplayName("Constructed Language Builder")
    
    # Load configuration
    config = Config()
    config.load()
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()