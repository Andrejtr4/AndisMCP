"""ANSI-Farb-Utilities für farbige Terminal-Ausgabe."""
import sys
import io

# Force UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Color:
    """ANSI Escape-Codes für Farben im Terminal."""
    BLUE = "\033[94m"      # Blau
    CYAN = "\033[96m"      # Cyan
    GREEN = "\033[92m"     # Grün
    YELLOW = "\033[93m"    # Gelb
    RED = "\033[91m"       # Rot
    WHITE = "\033[97m"     # Weiß
    RESET = "\033[0m"      # Zurücksetzen
    BOLD = "\033[1m"       # Fett

def print_header(text):
    """Druckt einen großen Header mit Rahmen."""
    print(f"\n{Color.BOLD}{Color.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Color.RESET}\n")

def print_section(text):
    """Druckt eine Sektion-Überschrift mit Pfeil."""
    print(f"{Color.BOLD}{Color.CYAN}► {text}{Color.RESET}")

def print_success(text):
    """Druckt eine Erfolgsmeldung in Grün mit Häkchen."""
    print(f"{Color.GREEN}✓ {text}{Color.RESET}")

def print_error(text):
    """Druckt eine Fehlermeldung in Rot mit X."""
    print(f"{Color.RED}✗ {text}{Color.RESET}")

def print_info(text):
    """Druckt eine Info-Meldung in Gelb mit Info-Symbol."""
    print(f"{Color.YELLOW}ℹ {text}{Color.RESET}")

def print_progress(text):
    """Druckt Fortschrittsmeldung in Cyan mit Pfeil."""
    print(f"{Color.CYAN}→ {text}{Color.RESET}")

def print_summary(text):
    """Druckt eine Zusammenfassung in Weiß/Fett."""
    print(f"\n{Color.BOLD}{Color.WHITE}{text}{Color.RESET}")
