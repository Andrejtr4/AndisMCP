"""ANSI color utilities for terminal output."""

class Color:
    """ANSI color codes."""
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def print_header(text):
    """Print header."""
    print(f"\n{Color.BOLD}{Color.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Color.RESET}\n")

def print_section(text):
    """Print section."""
    print(f"{Color.BOLD}{Color.CYAN}► {text}{Color.RESET}")

def print_success(text):
    """Print success."""
    print(f"{Color.GREEN}✓ {text}{Color.RESET}")

def print_error(text):
    """Print error."""
    print(f"{Color.RED}✗ {text}{Color.RESET}")

def print_info(text):
    """Print info."""
    print(f"{Color.YELLOW}ℹ {text}{Color.RESET}")

def print_progress(text):
    """Print progress."""
    print(f"{Color.CYAN}→ {text}{Color.RESET}")

def print_summary(text):
    """Print summary."""
    print(f"\n{Color.BOLD}{Color.WHITE}{text}{Color.RESET}")
