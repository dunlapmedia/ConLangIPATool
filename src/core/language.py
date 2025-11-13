"""
Enhanced language model and management system.
Handles language creation, storage, and manipulation with robust linguistic features.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class PartOfSpeech(Enum):
    """Enumeration of parts of speech."""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    ARTICLE = "article"
    NUMERAL = "numeral"
    PARTICLE = "particle"
    AUXILIARY = "auxiliary"
    DETERMINER = "determiner"
    POSTPOSITION = "postposition"


class WordOrder(Enum):
    """Enhanced word order patterns including direct and indirect objects."""

    SOV = "Subject-DirectObject-Verb"
    SVO = "Subject-Verb-DirectObject"
    VSO = "Verb-Subject-DirectObject"
    VOS = "Verb-DirectObject-Subject"
    OVS = "DirectObject-Verb-Subject"
    OSV = "DirectObject-Subject-Verb"
    S_V_DO_IO = "Subject-Verb-DirectObject-IndirectObject"
    S_V_IO_DO = "Subject-Verb-IndirectObject-DirectObject"
    S_IO_DO_V = "Subject-IndirectObject-DirectObject-Verb"
    S_DO_IO_V = "Subject-DirectObject-IndirectObject-Verb"
    V_S_IO_DO = "Verb-Subject-IndirectObject-DirectObject"
    V_S_DO_IO = "Verb-Subject-DirectObject-IndirectObject"
    S_IO_V_DO = "Subject-IndirectObject-Verb-DirectObject"
    IO_S_V_DO = "IndirectObject-Subject-Verb-DirectObject"


class StressPattern(Enum):
    """Primary stress patterns offered by the language creation wizard."""

    NO_FIXED = "No Fixed Stress"
    INITIAL = "Initial Syllable"
    SECOND = "Second Syllable"
    ANTEPENULTIMATE = "Antepenultimate"
    PENULTIMATE = "Penultimate"
    ULTIMATE = "Ultimate"
    NO_STRESS = "No Stress"
    CUSTOM_FOOT = "Custom Foot-Based Pattern"


class FootDirection(Enum):
    """Foot construction direction for custom stress patterns."""

    LEFT_TO_RIGHT = "left"
    RIGHT_TO_LEFT = "right"


class MainStressPosition(Enum):
    """Primary stress placement relative to foot structure."""

    LEFT_MOST = "left-most"
    RIGHT_MOST = "right-most"


@dataclass
class CustomStressPattern:
    """Configuration for custom foot-based stress rules."""

    foot_size: int = 2
    foot_direction: FootDirection = FootDirection.LEFT_TO_RIGHT
    stressed_syllable_in_foot: int = 1
    main_stress_position: MainStressPosition = MainStressPosition.RIGHT_MOST

    def validate(self) -> None:
        """Ensure the chosen parameters are internally consistent."""
        if self.foot_size not in (2, 3):
            raise ValueError("Foot size must be either 2 or 3 syllables.")
        if self.stressed_syllable_in_foot < 1 or self.stressed_syllable_in_foot > self.foot_size:
            raise ValueError("Stressed syllable must fall within the foot size.")


@dataclass
class StressSettings:
    """Stress configuration for a language."""

    pattern: StressPattern = StressPattern.NO_FIXED
    custom_pattern: Optional[CustomStressPattern] = None


@dataclass
class PhonotacticProfile:
    """Inventory and phonotactic restrictions for a language."""

    consonants: List[str] = field(default_factory=list)
    vowels: List[str] = field(default_factory=list)
    onset_clusters: List[str] = field(default_factory=list)
    medial_clusters: List[str] = field(default_factory=list)
    coda_clusters: List[str] = field(default_factory=list)
    illegal_sequences: List[str] = field(default_factory=list)


@dataclass
class LexiconEntry:
    """A single lexical entry for the working dictionary."""

    conlang: str
    part_of_speech: str
    english: str = ""
    ipa: str = ""


@dataclass
class AffixDefinition:
    """Simple affix description."""

    label: str
    description: str = ""


@dataclass
class DerivedWordDefinition:
    """Representation of a derived form based on base lexemes."""

    base: str
    derived_form: str
    gloss: str = ""


@dataclass
class GrammarProfile:
    """Grammar customization options."""

    word_order: WordOrder = WordOrder.SVO
    optional_parts_of_speech: List[PartOfSpeech] = field(default_factory=list)
    notes: str = ""


@dataclass
class LanguageProfile:
    """Aggregate configuration for a constructed language."""

    identifier: str
    name: Optional[str]
    generated_name: Optional[str]
    phonotactics: PhonotacticProfile
    stress: StressSettings
    lexicon: List[LexiconEntry] = field(default_factory=list)
    affixes: List[AffixDefinition] = field(default_factory=list)
    derived_words: List[DerivedWordDefinition] = field(default_factory=list)
    grammar: GrammarProfile = field(default_factory=GrammarProfile)

    @property
    def display_name(self) -> str:
        """Preferred display label for the language."""
        return self.name or self.generated_name or "Unnamed Language"

    @classmethod
    def create(
        cls,
        *,
        name: Optional[str],
        generated_name: Optional[str],
        phonotactics: PhonotacticProfile,
        stress: StressSettings,
        lexicon: Optional[List[LexiconEntry]] = None,
        affixes: Optional[List[AffixDefinition]] = None,
        derived_words: Optional[List[DerivedWordDefinition]] = None,
        grammar: Optional[GrammarProfile] = None,
    ) -> "LanguageProfile":
        """Convenience constructor that assigns an identifier."""
        return cls(
            identifier=str(uuid.uuid4()),
            name=name,
            generated_name=generated_name,
            phonotactics=phonotactics,
            stress=stress,
            lexicon=lexicon or [],
            affixes=affixes or [],
            derived_words=derived_words or [],
            grammar=grammar or GrammarProfile(),
        )


class IPAChart:
    """Complete IPA chart with proper Unicode characters."""

    pass

