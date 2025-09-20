"""
Configuration file for FormatFusion.
Contains application settings and constants.
"""

import os
from pathlib import Path

# Application information
APP_NAME = "FormatFusion"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Universal File Converter"

# File size limits (in bytes)
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
MAX_IMAGE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_AUDIO_SIZE = 500 * 1024 * 1024  # 500MB
MAX_VIDEO_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

# Supported file extensions
SUPPORTED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp'}
SUPPORTED_AUDIO_EXTENSIONS = {'.wav', '.m4a', '.flac', '.ogg', '.mp3', '.aac', '.wma'}
SUPPORTED_VIDEO_EXTENSIONS = {'.mkv', '.mov', '.avi', '.webm', '.flv', '.mp4', '.wmv', '.m4v'}

# FFmpeg paths to check
FFMPEG_PATHS = [
    'ffmpeg.exe',
    'bin/ffmpeg.exe',
    'resources/ffmpeg.exe'
]

# Default conversion settings
DEFAULT_IMAGE_FORMAT = 'png'
DEFAULT_AUDIO_QUALITY = '192'
DEFAULT_VIDEO_QUALITY = 'original'

# UI settings
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 500
WINDOW_DEFAULT_WIDTH = 800
WINDOW_DEFAULT_HEIGHT = 600

# Progress update interval (milliseconds)
PROGRESS_UPDATE_INTERVAL = 100

# Temporary directory for processing
TEMP_DIR = Path(os.environ.get('TEMP', '/tmp')) / 'formatfusion'

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Conversion timeouts (seconds)
CONVERSION_TIMEOUT = 300  # 5 minutes
FFMPEG_TIMEOUT = 10  # 10 seconds for FFmpeg version check
