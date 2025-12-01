"""Configuration for test generation quality."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class TestGenerationConfig:
    """Configure test generation behavior."""
    
    # Quality level
    quality: Literal["basic", "standard", "comprehensive"] = "standard"
    
    # Test types to generate
    include_happy_path: bool = True
    include_error_cases: bool = True
    include_edge_cases: bool = True
    include_accessibility: bool = False
    
    # AI enhancement
    enhance_pom: bool = True  # Auto-enhance POMs during generation
    enhance_tests: bool = True  # Generate AI-powered tests
    
    # AI model
    model: str = "gpt-4o-mini"
    temperature: float = 0.1
    
    # Code style
    use_type_hints: bool = True
    use_async: bool = True
    max_tests_per_page: int = 5
    
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
