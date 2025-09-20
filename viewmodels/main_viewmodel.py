"""
Main ViewModel for FormatFusion application.
Handles business logic and state management.
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path

from models.file_info import FileInfo, FileType
from models.conversion_options import ConversionOptions, ImageConversionOptions, AudioConversionOptions, VideoConversionOptions
from models.conversion_options import ImageFormat, AudioQuality, VideoQuality
from services.conversion_service import ConversionService


class ConversionWorker(QThread):
    """Worker thread for file conversion."""
    
    progress_updated = pyqtSignal(int)
    conversion_finished = pyqtSignal(bool, str)
    
    def __init__(self, file_info, options, output_path, conversion_service):
        super().__init__()
        self.file_info = file_info
        self.options = options
        self.output_path = output_path
        self.conversion_service = conversion_service
    
    def run(self):
        """Run conversion in background thread."""
        try:
            success = self.conversion_service.convert_file(
                self.file_info,
                self.options,
                self.output_path,
                self.progress_updated.emit
            )
            self.conversion_finished.emit(success, self.output_path)
        except Exception as e:
            self.conversion_finished.emit(False, str(e))


class MainViewModel(QObject):
    """Main ViewModel for the application."""
    
    # Signals
    file_loaded = pyqtSignal(FileInfo)
    file_cleared = pyqtSignal()
    conversion_options_changed = pyqtSignal()
    conversion_started = pyqtSignal()
    conversion_progress = pyqtSignal(int)
    conversion_finished = pyqtSignal(bool, str)
    status_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_file: FileInfo = None
        self.conversion_options: ConversionOptions = None
        self.conversion_service = ConversionService()
        self.conversion_worker: ConversionWorker = None
        
        # Initialize default options
        self._initialize_default_options()
    
    def _initialize_default_options(self):
        """Initialize default conversion options."""
        self.conversion_options = ConversionOptions(FileType.UNSUPPORTED)
    
    def load_file(self, file_path: str) -> bool:
        """Load a file and update the model."""
        try:
            file_info = FileInfo(file_path)
            if not file_info.is_valid:
                self.status_message.emit(f"Unsupported file type: {file_info.extension}")
                return False
            
            self.current_file = file_info
            self.conversion_options = ConversionOptions(file_info.file_type)
            self.file_loaded.emit(file_info)
            self.conversion_options_changed.emit()
            self.status_message.emit(f"File loaded: {file_info.filename}{file_info.extension}")
            return True
        except Exception as e:
            self.status_message.emit(f"Error loading file: {str(e)}")
            return False
    
    def clear_file(self):
        """Clear current file and reset state."""
        self.current_file = None
        self.conversion_options = None
        self.file_cleared.emit()
        self.conversion_options_changed.emit()
        self.status_message.emit("Ready")
    
    def select_file(self) -> str:
        """Open file dialog to select a file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None,
            "Select File to Convert",
            "",
            "All Files (*.*);;Images (*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.webp);;"
            "Audio (*.wav *.m4a *.flac *.ogg *.mp3 *.aac *.wma);;"
            "Video (*.mkv *.mov *.avi *.webm *.flv *.mp4 *.wmv *.m4v)"
        )
        return file_path
    
    def update_image_format(self, format_value: str):
        """Update image output format."""
        if self.conversion_options and self.conversion_options.image_options:
            self.conversion_options.image_options.output_format = ImageFormat(format_value)
            self.conversion_options_changed.emit()
    
    def update_image_resize(self, enabled: bool, max_width: int = None, max_height: int = None):
        """Update image resize options."""
        if self.conversion_options and self.conversion_options.image_options:
            self.conversion_options.image_options.resize_enabled = enabled
            if enabled:
                self.conversion_options.image_options.max_width = max_width
                self.conversion_options.image_options.max_height = max_height
            self.conversion_options_changed.emit()
    
    def update_image_size_limit(self, enabled: bool, max_size_kb: int = None):
        """Update image size limit options."""
        if self.conversion_options and self.conversion_options.image_options:
            self.conversion_options.image_options.size_limit_enabled = enabled
            if enabled:
                self.conversion_options.image_options.max_size_kb = max_size_kb
            self.conversion_options_changed.emit()
    
    def update_audio_quality(self, quality_value: str):
        """Update audio quality setting."""
        if self.conversion_options and self.conversion_options.audio_options:
            self.conversion_options.audio_options.quality = AudioQuality(quality_value)
            self.conversion_options_changed.emit()
    
    def update_video_quality(self, quality_value: str):
        """Update video quality setting."""
        if self.conversion_options and self.conversion_options.video_options:
            self.conversion_options.video_options.quality = VideoQuality(quality_value)
            self.conversion_options_changed.emit()
    
    def update_video_fast_mode(self, fast_mode: bool):
        """Update video fast mode setting."""
        if self.conversion_options and self.conversion_options.video_options:
            self.conversion_options.video_options.fast_mode = fast_mode
            self.conversion_options_changed.emit()
    
    def can_convert(self) -> bool:
        """Check if conversion can be performed."""
        return (self.current_file is not None and 
                self.conversion_options is not None and 
                self.conversion_options.is_valid())
    
    def start_conversion(self, output_path: str):
        """Start file conversion in background thread."""
        if not self.can_convert():
            self.status_message.emit("Cannot convert: Invalid file or options")
            return
        
        if self.conversion_worker and self.conversion_worker.isRunning():
            self.status_message.emit("Conversion already in progress")
            return
        
        self.conversion_worker = ConversionWorker(
            self.current_file,
            self.conversion_options,
            output_path,
            self.conversion_service
        )
        
        self.conversion_worker.progress_updated.connect(self.conversion_progress.emit)
        self.conversion_worker.conversion_finished.connect(self._on_conversion_finished)
        
        self.conversion_worker.start()
        self.conversion_started.emit()
        self.status_message.emit("Converting file...")
    
    @pyqtSlot(bool, str)
    def _on_conversion_finished(self, success: bool, message: str):
        """Handle conversion completion."""
        if success:
            self.status_message.emit("Conversion complete!")
            self.conversion_finished.emit(True, message)
        else:
            self.status_message.emit(f"Conversion failed: {message}")
            self.conversion_finished.emit(False, message)
    
    def get_output_filename(self) -> str:
        """Generate output filename based on current file and options."""
        if not self.current_file:
            return ""
        
        base_name = self.current_file.filename
        input_dir = self.current_file.file_path.parent
        
        if self.current_file.file_type == FileType.IMAGE:
            if self.conversion_options and self.conversion_options.image_options:
                extension = self.conversion_options.image_options.output_format.value
            else:
                extension = "png"
        elif self.current_file.file_type == FileType.AUDIO:
            extension = "mp3"
        elif self.current_file.file_type == FileType.VIDEO:
            extension = "mp4"
        else:
            extension = self.current_file.extension[1:]  # Remove dot
        
        # Return full path in the same directory as input file
        return str(input_dir / f"{base_name}_converted.{extension}")
