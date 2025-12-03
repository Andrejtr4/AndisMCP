"""Konfigurations-Klasse für die Qualität der Test-Generierung."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class TestGenerationConfig:
    """
    Konfiguriert das Verhalten der Test-Generierung.
    
    Steuert Qualitätsstufen, AI-Enhancement und Test-Typen.
    """
    
    # Qualitätsstufe: basic (schnell), standard (balanced), comprehensive (vollständig)
    quality: Literal["basic", "standard", "comprehensive"] = "standard"
    
    # Welche Test-Typen sollen generiert werden?
    include_happy_path: bool = True      # Normale Benutzung
    include_error_cases: bool = True     # Fehlerszenarien
    include_edge_cases: bool = True      # Grenzfälle
    include_accessibility: bool = False  # Barrierefreiheit-Tests
    
    # KI-Verbesserung aktivieren?
    enhance_pom: bool = True   # POMs automatisch mit KI verbessern
    enhance_tests: bool = True # Tests mit KI-Power generieren
    
    # Welches KI-Modell nutzen?
    model: str = "gpt-4o-mini"
    temperature: float = 0.1   # Niedrige Temperatur = deterministischer
    
    # Code-Style-Einstellungen
    use_type_hints: bool = True  # Type-Hints in generiertem Code
    use_async: bool = True       # Async/await nutzen
    max_tests_per_page: int = 5  # Maximale Anzahl Tests pro Seite
    
    @classmethod
    def basic(cls):
        """Basic test generation - only happy path, no AI enhancement."""
        return cls(
            quality="basic",
            include_error_cases=False,
            include_edge_cases=False,
            enhance_pom=False,  # Skip AI enhancement for speed
            enhance_tests=False,  # Use templates for speed
            model="gpt-4o-mini",
        )
    
    @classmethod
    def comprehensive(cls):
        """Comprehensive testing with all checks and full AI enhancement."""
        return cls(
            quality="comprehensive",
            include_accessibility=True,
            enhance_pom=True,
            enhance_tests=True,
            model="gpt-4o",
            max_tests_per_page=10,
        )


# Default configuration
DEFAULT_CONFIG = TestGenerationConfig()
