"""
Utility functions for file operations.
"""

import os
import shutil
from pathlib import Path
from typing import Optional


def get_file_icon_path(file_extension: str) -> Optional[str]:
    """Get icon path for file extension."""
    icon_dir = Path("icons")
    if not icon_dir.exists():
        return None
    
    extension = file_extension.lower().lstrip('.')
    icon_path = icon_dir / f"{extension}.ico"
    
    if icon_path.exists():
        return str(icon_path)
    
    # Default icon
    default_icon = icon_dir / "default.ico"
    if default_icon.exists():
        return str(default_icon)
    
    return None


def ensure_directory_exists(path: str) -> bool:
    """Ensure directory exists, create if necessary."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False


def get_safe_filename(filename: str) -> str:
    """Get a safe filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_unique_filename(file_path: str) -> str:
    """Get a unique filename if the file already exists."""
    path = Path(file_path)
    if not path.exists():
        return file_path
    
    counter = 1
    while True:
        new_path = path.parent / f"{path.stem}_{counter}{path.suffix}"
        if not new_path.exists():
            return str(new_path)
        counter += 1


def copy_file_with_progress(src: str, dst: str, progress_callback=None) -> bool:
    """Copy file with optional progress callback."""
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        # Ensure destination directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(src_path, dst_path)
        
        if progress_callback:
            progress_callback(100)
        
        return True
    except Exception as e:
        print(f"File copy error: {e}")
        return False
