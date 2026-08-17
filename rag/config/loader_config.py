"""
Configuration classes for the Unified RAG Pipeline.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session

@dataclass
class LoaderConfig:
    """configuration for document loader"""

     # Source information
    source_type: str
    source_name: Optional[str] = None

    # Database
    session: Optional[Session] = None
    table_name: Optional[str] = None

    user_id:int |None=None

    # Files
    file_path: Optional[Path] = None

    # Generic text extraction
    text_column: Optional[str] = None

    # Metadata columns to include
    metadata_columns: list[str] | None = None
