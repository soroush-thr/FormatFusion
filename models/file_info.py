"""
File information model for FormatFusion.
Represents file metadata and type information.
"""

from enum import Enum
from pathlib import Path
from typing import Optional


class FileType(Enum):
    """Supported file types for conversion."""
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNSUPPORTED = "unsupported"


class ImageFormat(Enum):
    """Supported image output formats."""
    JPG = "jpg"
    PNG = "png"


class AudioQuality(Enum):
    """Audio quality presets."""
    STANDARD = "128"
    GOOD = "192"
    HIGH = "256"
    LOSSLESS = "320"


class VideoQuality(Enum):
    """Video quality presets."""
    SD_480P = "480p"
    HD_720P = "720p"
    FHD_1080P = "1080p"
    ORIGINAL = "original"


class FileInfo:
    """Model representing file information and metadata."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_type = self._detect_file_type()
        self.file_size = self._get_file_size()
        self.is_valid = self.file_type != FileType.UNSUPPORTED
    
    def _detect_file_type(self) -> FileType:
        """Detect file type based on extension."""
        extension = self.file_path.suffix.lower()
        
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp'}
        audio_extensions = {'.wav', '.m4a', '.flac', '.ogg', '.mp3', '.aac', '.wma'}
        video_extensions = {'.mkv', '.mov', '.avi', '.webm', '.flv', '.mp4', '.wmv', '.m4v'}
        
        if extension in image_extensions:
            return FileType.IMAGE
        elif extension in audio_extensions:
            return FileType.AUDIO
        elif extension in video_extensions:
            return FileType.VIDEO
        else:
            return FileType.UNSUPPORTED
    
    def _get_file_size(self) -> int:
        """Get file size in bytes."""
        try:
            return self.file_path.stat().st_size
        except (OSError, FileNotFoundError):
            return 0
    
    @property
    def filename(self) -> str:
        """Get filename without extension."""
        return self.file_path.stem
    
    @property
    def extension(self) -> str:
        """Get file extension."""
        return self.file_path.suffix
    
    @property
    def size_formatted(self) -> str:
        """Get formatted file size string."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def __str__(self) -> str:
        return f"FileInfo({self.filename}{self.extension}, {self.file_type.value}, {self.size_formatted})"
