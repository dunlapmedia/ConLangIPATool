# ConLang IPA Tool

This project is a tool for creating constructed languages with complete IPA (International Phonetic Alphabet) support, grammar tooling, and text-to-speech helpers.

## Features
- Enhanced language model with advanced word order handling and IPA data
- Grammar editing tools, translation workflow, and dictionary management
- Modular PyQt6 interface with dedicated widgets for each workflow

## Project Structure
```
ConLangIPATool/
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
└── src/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── language.py          ✅ Enhanced word order + IPA
    │   ├── config.py
    │   ├── logger.py
    │   ├── grammar_parser.py
    │   ├── tts_engine.py
    │   ├── translator.py
    │   └── evolution.py
    ├── ui/
    │   ├── __init__.py
    │   └── main_window.py
    └── widgets/
        ├── __init__.py
        ├── dictionary_widget.py
        ├── ipa_input_widget.py
        ├── grammar_editor.py
        ├── translator_widget.py
        └── tts_widget.py
```

## Installation
Use the `requirements.txt` file to install the necessary packages.
