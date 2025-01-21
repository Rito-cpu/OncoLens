import os
import mimetypes

from typing import Optional



def is_json_file(filepath: str) -> bool:
    """Check if the file has a JSON mime type."""
    mime_type, _ = mimetypes.guess_type(filepath)

    return mime_type == "application/json"

def is_valid_json_file(filepath: str) -> bool:
    """Check if the file is a valid JSON file."""

    return is_json_file(filepath) and os.path.exists(filepath)

def is_excel_file(filepath: str) -> bool:
    """Check if the file has an Excel mime type."""
    mime_type, _ = mimetypes.guess_type(filepath)
    target_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return mime_type == target_type

def is_valid_excel_file(filepath: str) -> bool:
    """Check if the file is a valid Excel file."""

    return is_excel_file(filepath) and os.path.exists(filepath)

def is_blank_line(line: Optional[str]) -> bool:
    """Check if the line is blank or None."""

    return line is None or not line.strip()
