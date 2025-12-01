"""Node: verify generated POM file."""

import subprocess
from pathlib import Path


def verify_pom(pom_path: str) -> tuple[bool, str]:
    """Verify POM file syntax."""
    pom_file = Path(pom_path)
    
    if not pom_file.exists():
        return False, f"File not found: {pom_path}"

    try:
        result = subprocess.run(
            ["python", "-m", "py_compile", str(pom_file)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False, f"Syntax error: {result.stderr}"
        return True, "OK"
    except Exception as e:
        return False, f"Error: {e}"
