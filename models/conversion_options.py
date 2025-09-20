"""
Conversion options model for FormatFusion.
Represents user-selected conversion parameters.
"""

from dataclasses import dataclass
from typing import Optional

from .file_info import FileType, ImageFormat, AudioQuality, VideoQuality


@dataclass
class ImageConversionOptions:
    """Options for image conversion."""
    output_format: ImageFormat
    resize_enabled: bool = False
    max_width: Optional[int] = None
    max_height: Optional[int] = None
    size_limit_enabled: bool = False
    max_size_kb: Optional[int] = None


@dataclass
class AudioConversionOptions:
    """Options for audio conversion."""
    quality: AudioQuality = AudioQuality.GOOD


@dataclass
class VideoConversionOptions:
    """Options for video conversion."""
    quality: VideoQuality = VideoQuality.ORIGINAL
    fast_mode: bool = True  # Enable fast conversion by default


@dataclass
class ConversionOptions:
    """Main conversion options container."""
    file_type: FileType
    image_options: Optional[ImageConversionOptions] = None
    audio_options: Optional[AudioConversionOptions] = None
    video_options: Optional[VideoConversionOptions] = None
    
    def __post_init__(self):
        """Initialize specific options based on file type."""
        if self.file_type == FileType.IMAGE and self.image_options is None:
            self.image_options = ImageConversionOptions(ImageFormat.PNG)
        elif self.file_type == FileType.AUDIO and self.audio_options is None:
            self.audio_options = AudioConversionOptions()
        elif self.file_type == FileType.VIDEO and self.video_options is None:
            self.video_options = VideoConversionOptions()
    
    def is_valid(self) -> bool:
        """Check if conversion options are valid."""
        if self.file_type == FileType.UNSUPPORTED:
            return False
        
        if self.file_type == FileType.IMAGE:
            return self.image_options is not None
        elif self.file_type == FileType.AUDIO:
            return self.audio_options is not None
        elif self.file_type == FileType.VIDEO:
            return self.video_options is not None
        
        return False
