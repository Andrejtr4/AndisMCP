"""Pydantic schemas."""

from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class PageJob(BaseModel):
    """Single page job in the pipeline."""
    url: str
    dom: str = ""
    model: Optional[Dict[str, Any]] = None
    pom_path: Optional[str] = None
    test_path: Optional[str] = None
    errors: List[str] = []


class Ctx(BaseModel):
    """LangGraph context state."""
    base_url: str
    max_pages: int = 10
    stories: str = ""
    links: List[str] = []
    jobs: Dict[str, PageJob] = {}
    total_processed: int = 0
    total_errors: int = 0
    errors: List[str] = []
