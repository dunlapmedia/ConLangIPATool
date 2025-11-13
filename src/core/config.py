"""
Configuration management for ConLang IPA Tool
"""

import os
import json
from pathlib import Path


class Config:
    """Configuration manager for the application"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".conlang_ipa_tool"
        self.config_file = self.config_dir / "config.json"
        self.settings = {
            "theme": "default",
            "recent_files": [],
            "auto_save": True,
            "language": "en"
        }
    
    def load(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.settings.update(json.load(f))
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save(self):
        """Save configuration to file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value"""
        self.settings[key] = value
