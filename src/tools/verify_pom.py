"""Tool zur Validierung von POM-Dateien auf Syntax-Fehler."""

import subprocess
from pathlib import Path


def verify_pom(pom_path: str) -> tuple[bool, str]:
    """
    Überprüft die Syntax einer POM-Datei mit Python-Compiler.
    
    Args:
        pom_path: Pfad zur zu überprüfenden POM-Datei
    
    Returns:
        Tuple mit (ist_valid, fehlermeldung_oder_ok)
    """
    pom_file = Path(pom_path)
    
    # Prüfe ob Datei existiert
    if not pom_file.exists():
        return False, f"File not found: {pom_path}"

    try:
        # Nutze Python's py_compile um Syntax zu prüfen
        result = subprocess.run(
            ["python", "-m", "py_compile", str(pom_file)],
            capture_output=True,  # Fange stdout/stderr ab
            text=True,            # Text statt Bytes
            timeout=10,           # Max 10 Sekunden
        )
        
        # Prüfe Exit-Code (0 = Erfolg, != 0 = Fehler)
        if result.returncode != 0:
            return False, f"Syntax error: {result.stderr}"
        
        return True, "OK"
    except Exception as e:
        return False, f"Error: {e}"
