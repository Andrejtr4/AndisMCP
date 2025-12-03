"""Pydantic-Schemas für Datenstrukturen in der Pipeline."""

from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class PageJob(BaseModel):
    """
    Repräsentiert einen einzelnen Seiten-Job in der Pipeline.
    
    Speichert alle Daten für eine zu verarbeitende Seite:
    - URL, DOM-Inhalt, extrahiertes Modell
    - Pfade zu generierten POMs und Tests
    - Aufgetretene Fehler
    """
    url: str                                 # URL der Seite
    dom: str = ""                           # HTML/DOM-Inhalt
    model: Optional[Dict[str, Any]] = None  # Extrahiertes UI-Modell
    pom_path: Optional[str] = None          # Pfad zum generierten POM
    test_path: Optional[str] = None         # Pfad zu generierten Tests
    errors: List[str] = []                  # Liste von Fehlern


class Ctx(BaseModel):
    """
    LangGraph Kontext-Zustand (State).
    
    Wird durch alle Pipeline-Nodes durchgereicht und speichert:
    - Basis-Konfiguration (URL, max_pages, stories)
    - Gefundene Links
    - Alle Jobs (PageJob pro URL)
    - Statistiken (verarbeitete Seiten, Fehler)
    """
    base_url: str                       # Start-URL für Crawling
    max_pages: int = 10                 # Maximale Anzahl zu verarbeitender Seiten
    stories: str = ""                   # Optionale User Stories für Tests
    links: List[str] = []               # Alle gefundenen Links
    jobs: Dict[str, PageJob] = {}       # URL -> PageJob Mapping
    total_processed: int = 0            # Anzahl erfolgreich verarbeiteter Seiten
    total_errors: int = 0               # Anzahl Fehler
    errors: List[str] = []              # Globale Fehlerliste
