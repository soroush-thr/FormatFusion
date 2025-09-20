"""
Main window view for FormatFusion application.
Implements the drag-and-drop interface and conversion controls.
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QSpinBox, QProgressBar, QFileDialog, QGroupBox,
    QGridLayout, QFrame, QSizePolicy, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSlot, QMimeData, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QDragEnterEvent, QDropEvent, QIcon

from models.file_info import FileType
from viewmodels.main_viewmodel import MainViewModel


class ThemeManager:
    """Manages the application's dark theme with navy-blue colors."""
    
    # Color palette
    COLORS = {
        'primary': '#1e3a8a',      # Navy blue
        'primary_dark': '#1e40af', # Darker navy
        'primary_light': '#3b82f6', # Light navy
        'secondary': '#0f172a',    # Very dark blue
        'accent': '#06b6d4',       # Cyan accent
        'accent_light': '#67e8f9', # Light cyan
        'background': '#0f172a',   # Dark background
        'surface': '#1e293b',      # Card surface
        'surface_light': '#334155', # Lighter surface
        'text_primary': '#f8fafc', # White text
        'text_secondary': '#cbd5e1', # Light gray text
        'text_muted': '#64748b',   # Muted text
        'border': '#475569',       # Border color
        'success': '#10b981',      # Green
        'warning': '#f59e0b',      # Orange
        'error': '#ef4444',        # Red
        'hover': '#334155',        # Hover state
        'pressed': '#475569',      # Pressed state
    }
    
    @classmethod
    def get_stylesheet(cls):
        """Get the complete application stylesheet."""
        return f"""
        /* Main Application */
        QMainWindow {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
        }}
        
        /* Drag and Drop Area */
        DragDropArea {{
            border: 3px dashed {cls.COLORS['border']};
            border-radius: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.COLORS['surface']}, 
                stop:1 {cls.COLORS['surface_light']});
            min-height: 200px;
        }}
        
        DragDropArea:hover {{
            border-color: {cls.COLORS['accent']};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {cls.COLORS['surface_light']}, 
                stop:1 {cls.COLORS['primary']});
        }}
        
        /* Buttons */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary']}, 
                stop:1 {cls.COLORS['primary_dark']});
            color: {cls.COLORS['text_primary']};
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary_light']}, 
                stop:1 {cls.COLORS['primary']});
        }}
        
        QPushButton:pressed {{
            background: {cls.COLORS['primary_dark']};
        }}
        
        QPushButton:disabled {{
            background: {cls.COLORS['surface_light']};
            color: {cls.COLORS['text_muted']};
        }}
        
        /* Secondary Button */
        QPushButton#secondary {{
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_secondary']};
            border: 1px solid {cls.COLORS['border']};
        }}
        
        QPushButton#secondary:hover {{
            background: {cls.COLORS['hover']};
            border-color: {cls.COLORS['accent']};
        }}
        
        /* Group Boxes */
        QGroupBox {{
            font-weight: bold;
            font-size: 14px;
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 10px;
            margin-top: 10px;
            padding-top: 10px;
            background: {cls.COLORS['surface']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
            color: {cls.COLORS['accent']};
        }}
        
        /* Labels */
        QLabel {{
            color: {cls.COLORS['text_primary']};
        }}
        
        QLabel#title {{
            font-size: 18px;
            font-weight: bold;
            color: {cls.COLORS['accent']};
        }}
        
        QLabel#subtitle {{
            font-size: 12px;
            color: {cls.COLORS['text_secondary']};
        }}
        
        /* Combo Boxes */
        QComboBox {{
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 8px 12px;
            min-width: 120px;
        }}
        
        QComboBox:hover {{
            border-color: {cls.COLORS['accent']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {cls.COLORS['text_secondary']};
            margin-right: 5px;
        }}
        
        QComboBox QAbstractItemView {{
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            selection-background-color: {cls.COLORS['primary']};
        }}
        
        /* Check Boxes */
        QCheckBox {{
            color: {cls.COLORS['text_primary']};
            font-size: 13px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {cls.COLORS['border']};
            border-radius: 4px;
            background: {cls.COLORS['surface']};
        }}
        
        QCheckBox::indicator:checked {{
            background: {cls.COLORS['accent']};
            border-color: {cls.COLORS['accent']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {cls.COLORS['accent']};
        }}
        
        /* Spin Boxes */
        QSpinBox {{
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 8px;
            min-width: 80px;
        }}
        
        QSpinBox:hover {{
            border-color: {cls.COLORS['accent']};
        }}
        
        QSpinBox:focus {{
            border-color: {cls.COLORS['accent']};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 2px solid {cls.COLORS['border']};
            border-radius: 8px;
            text-align: center;
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {cls.COLORS['accent']}, 
                stop:1 {cls.COLORS['accent_light']});
            border-radius: 6px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background: {cls.COLORS['surface']};
            color: {cls.COLORS['text_secondary']};
            border-top: 1px solid {cls.COLORS['border']};
        }}
        
        /* File Info Widget */
        QWidget#fileInfo {{
            background: {cls.COLORS['surface']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 10px;
            padding: 15px;
        }}
        
        /* Dialog Boxes */
        QDialog {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
        }}
        
        QMessageBox {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
        }}
        
        QMessageBox QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary']}, 
                stop:1 {cls.COLORS['primary_dark']});
            color: {cls.COLORS['text_primary']};
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            min-width: 80px;
        }}
        
        QMessageBox QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary_light']}, 
                stop:1 {cls.COLORS['primary']});
        }}
        
        QMessageBox QLabel {{
            color: {cls.COLORS['text_primary']};
            background-color: transparent;
        }}
        
        /* File Dialog */
        QFileDialog {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
        }}
        
        QFileDialog QWidget {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
        }}
        
        QFileDialog QListView {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
        }}
        
        QFileDialog QListView::item {{
            padding: 5px;
            border-bottom: 1px solid {cls.COLORS['border']};
        }}
        
        QFileDialog QListView::item:selected {{
            background-color: {cls.COLORS['primary']};
        }}
        
        QFileDialog QListView::item:hover {{
            background-color: {cls.COLORS['hover']};
        }}
        
        QFileDialog QLineEdit {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        QFileDialog QLineEdit:focus {{
            border-color: {cls.COLORS['accent']};
        }}
        
        QFileDialog QComboBox {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        QFileDialog QComboBox:hover {{
            border-color: {cls.COLORS['accent']};
        }}
        
        QFileDialog QComboBox QAbstractItemView {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            selection-background-color: {cls.COLORS['primary']};
        }}
        
        QFileDialog QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary']}, 
                stop:1 {cls.COLORS['primary_dark']});
            color: {cls.COLORS['text_primary']};
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            min-width: 80px;
        }}
        
        QFileDialog QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {cls.COLORS['primary_light']}, 
                stop:1 {cls.COLORS['primary']});
        }}
        
        QFileDialog QPushButton:pressed {{
            background: {cls.COLORS['primary_dark']};
        }}
        
        QFileDialog QPushButton:disabled {{
            background: {cls.COLORS['surface_light']};
            color: {cls.COLORS['text_muted']};
        }}
        
        /* Tool Tips */
        QToolTip {{
            background-color: {cls.COLORS['surface']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 4px;
            padding: 5px;
        }}
        """
    
    @classmethod
    def apply_theme(cls, app):
        """Apply the dark theme to the application."""
        app.setStyleSheet(cls.get_stylesheet())


class DragDropArea(QFrame):
    """Custom drag and drop area widget."""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(0)  # Remove default border, using CSS instead
        
        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Add logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(80, 80)
        self._load_logo()
        
        # Add title
        self.title_label = QLabel("FormatFusion")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title")
        
        # Add subtitle
        self.subtitle_label = QLabel("Drag & Drop a File Here, or Click to Select")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("subtitle")
        
        # Add supported formats
        self.formats_label = QLabel("Supports: Images • Audio • Video")
        self.formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formats_label.setObjectName("subtitle")
        
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.formats_label)
        self.setLayout(layout)
    
    def _load_logo(self):
        """Load the application logo."""
        import sys
        
        # Get the correct path for bundled resources
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        logo_paths = [
            os.path.join(base_path, "resources", "logo.png"),
            os.path.join(base_path, "logo.png"),
            os.path.join(base_path, "assets", "logo.png"),
            "resources/logo.png",  # Fallback for development
            "logo.png",
            "assets/logo.png"
        ]
        
        logo_loaded = False
        for path in logo_paths:
            if os.path.exists(path):
                try:
                    pixmap = QPixmap(path)
                    if not pixmap.isNull():
                        # Scale logo to fit
                        scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        self.logo_label.setPixmap(scaled_pixmap)
                        logo_loaded = True
                        print(f"Logo loaded from: {path}")  # Debug info
                        break
                except Exception as e:
                    print(f"Error loading logo from {path}: {e}")
                    continue
        
        if not logo_loaded:
            # Fallback to text logo
            self.logo_label.setText("🔄")
            self.logo_label.setStyleSheet("font-size: 48px; color: #06b6d4;")
            print("Using fallback text logo")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # The hover effect is handled by CSS
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        # The styling is handled by CSS, no need to reset here
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                self.file_dropped.emit(file_path)
    
    def mousePressEvent(self, event):
        """Handle mouse press to open file dialog."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.file_dropped.emit("")  # Empty string triggers file dialog


class FileInfoWidget(QWidget):
    """Widget to display file information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("fileInfo")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for file information display."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # File icon and name
        self.file_icon = QLabel()
        self.file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_icon.setFixedSize(80, 80)
        
        self.file_name = QLabel()
        self.file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_name.setObjectName("title")
        
        self.file_size = QLabel()
        self.file_size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_size.setObjectName("subtitle")
        
        layout.addWidget(self.file_icon)
        layout.addWidget(self.file_name)
        layout.addWidget(self.file_size)
        
        self.setLayout(layout)
    
    def update_file_info(self, file_info):
        """Update display with file information."""
        if file_info:
            # Set file icon based on type
            if file_info.file_type == FileType.IMAGE:
                icon_text = "🖼️"
            elif file_info.file_type == FileType.AUDIO:
                icon_text = "🎵"
            elif file_info.file_type == FileType.VIDEO:
                icon_text = "🎬"
            else:
                icon_text = "📄"
            
            self.file_icon.setText(icon_text)
            self.file_icon.setStyleSheet("font-size: 48px;")
            
            self.file_name.setText(f"{file_info.filename}{file_info.extension}")
            self.file_size.setText(file_info.size_formatted)
        else:
            self.file_icon.setText("")
            self.file_name.setText("")
            self.file_size.setText("")


class ConversionOptionsWidget(QWidget):
    """Widget for conversion options based on file type."""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_type = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for conversion options."""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Initially hidden
        self.setVisible(False)
    
    def update_for_file_type(self, file_type: FileType):
        """Update options based on file type."""
        self.current_file_type = file_type
        
        # Clear existing widgets
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        
        if file_type == FileType.IMAGE:
            self._setup_image_options()
        elif file_type == FileType.AUDIO:
            self._setup_audio_options()
        elif file_type == FileType.VIDEO:
            self._setup_video_options()
        else:
            self.setVisible(False)
            return
        
        self.setVisible(True)
    
    def _setup_image_options(self):
        """Setup image conversion options."""
        group = QGroupBox("Image Conversion Options")
        layout = QVBoxLayout()
        
        # Output format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPG"])
        self.format_combo.currentTextChanged.connect(self._on_options_changed)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        layout.addLayout(format_layout)
        
        # Resize options
        self.resize_checkbox = QCheckBox("Resize Image")
        self.resize_checkbox.toggled.connect(self._on_resize_toggled)
        layout.addWidget(self.resize_checkbox)
        
        # Resize dimensions
        resize_layout = QHBoxLayout()
        resize_layout.addWidget(QLabel("Max Width:"))
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10000)
        self.width_spinbox.setValue(1920)
        self.width_spinbox.setEnabled(False)
        self.width_spinbox.valueChanged.connect(self._on_options_changed)
        resize_layout.addWidget(self.width_spinbox)
        
        resize_layout.addWidget(QLabel("Max Height:"))
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 10000)
        self.height_spinbox.setValue(1080)
        self.height_spinbox.setEnabled(False)
        self.height_spinbox.valueChanged.connect(self._on_options_changed)
        resize_layout.addWidget(self.height_spinbox)
        resize_layout.addStretch()
        layout.addLayout(resize_layout)
        
        # Size limit options
        self.size_limit_checkbox = QCheckBox("Limit File Size")
        self.size_limit_checkbox.toggled.connect(self._on_size_limit_toggled)
        layout.addWidget(self.size_limit_checkbox)
        
        # Size limit input
        size_limit_layout = QHBoxLayout()
        size_limit_layout.addWidget(QLabel("Max Size (KB):"))
        self.size_limit_spinbox = QSpinBox()
        self.size_limit_spinbox.setRange(1, 10000)
        self.size_limit_spinbox.setValue(500)
        self.size_limit_spinbox.setEnabled(False)
        self.size_limit_spinbox.valueChanged.connect(self._on_options_changed)
        size_limit_layout.addWidget(self.size_limit_spinbox)
        size_limit_layout.addStretch()
        layout.addLayout(size_limit_layout)
        
        group.setLayout(layout)
        self.layout.addWidget(group)
    
    def _setup_audio_options(self):
        """Setup audio conversion options."""
        group = QGroupBox("Audio Conversion Options")
        layout = QVBoxLayout()
        
        # Quality selection
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Audio Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "128 kbps (Standard)",
            "192 kbps (Good)",
            "256 kbps (High Quality)",
            "320 kbps (Lossless Quality)"
        ])
        self.quality_combo.setCurrentIndex(1)  # Default to "Good"
        self.quality_combo.currentTextChanged.connect(self._on_options_changed)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
        # Output format info
        info_label = QLabel("Output Format: MP3")
        info_label.setStyleSheet("color: #666666; font-style: italic;")
        layout.addWidget(info_label)
        
        group.setLayout(layout)
        self.layout.addWidget(group)
    
    def _setup_video_options(self):
        """Setup video conversion options."""
        group = QGroupBox("Video Conversion Options")
        layout = QVBoxLayout()
        
        # Quality selection
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Video Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "480p (Standard Definition)",
            "720p (HD)",
            "1080p (Full HD)",
            "Original (Keep source quality)"
        ])
        self.quality_combo.setCurrentIndex(3)  # Default to "Original"
        self.quality_combo.currentTextChanged.connect(self._on_options_changed)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        layout.addLayout(quality_layout)
        
        # Fast mode option
        self.fast_mode_checkbox = QCheckBox("Fast Conversion (Recommended)")
        self.fast_mode_checkbox.setChecked(True)  # Default to fast mode
        self.fast_mode_checkbox.setToolTip("Enable fast conversion for significantly faster processing. Slight quality reduction but much faster encoding.")
        self.fast_mode_checkbox.toggled.connect(self._on_options_changed)
        layout.addWidget(self.fast_mode_checkbox)
        
        # Output format info
        info_label = QLabel("Output Format: MP4")
        info_label.setStyleSheet("color: #666666; font-style: italic;")
        layout.addWidget(info_label)
        
        group.setLayout(layout)
        self.layout.addWidget(group)
    
    def _on_resize_toggled(self, checked):
        """Handle resize checkbox toggle."""
        self.width_spinbox.setEnabled(checked)
        self.height_spinbox.setEnabled(checked)
        self._on_options_changed()
    
    def _on_size_limit_toggled(self, checked):
        """Handle size limit checkbox toggle."""
        self.size_limit_spinbox.setEnabled(checked)
        self._on_options_changed()
    
    def _on_options_changed(self):
        """Emit options changed signal."""
        self.options_changed.emit()
    
    def get_image_options(self):
        """Get current image options."""
        if self.current_file_type != FileType.IMAGE:
            return None
        
        format_text = self.format_combo.currentText().lower()
        resize_enabled = self.resize_checkbox.isChecked()
        max_width = self.width_spinbox.value() if resize_enabled else None
        max_height = self.height_spinbox.value() if resize_enabled else None
        size_limit_enabled = self.size_limit_checkbox.isChecked()
        max_size_kb = self.size_limit_spinbox.value() if size_limit_enabled else None
        
        return {
            'format': format_text,
            'resize_enabled': resize_enabled,
            'max_width': max_width,
            'max_height': max_height,
            'size_limit_enabled': size_limit_enabled,
            'max_size_kb': max_size_kb
        }
    
    def get_audio_options(self):
        """Get current audio options."""
        if self.current_file_type != FileType.AUDIO:
            return None
        
        quality_text = self.quality_combo.currentText()
        if "128" in quality_text:
            quality = "128"
        elif "192" in quality_text:
            quality = "192"
        elif "256" in quality_text:
            quality = "256"
        elif "320" in quality_text:
            quality = "320"
        else:
            quality = "192"
        
        return {'quality': quality}
    
    def get_video_options(self):
        """Get current video options."""
        if self.current_file_type != FileType.VIDEO:
            return None
        
        quality_text = self.quality_combo.currentText()
        if "480p" in quality_text:
            quality = "480p"
        elif "720p" in quality_text:
            quality = "720p"
        elif "1080p" in quality_text:
            quality = "1080p"
        else:
            quality = "original"
        
        fast_mode = self.fast_mode_checkbox.isChecked()
        
        return {'quality': quality, 'fast_mode': fast_mode}


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.viewmodel = MainViewModel()
        self.setup_ui()
        self.connect_signals()
        self.setWindowTitle("FormatFusion - File Converter")
        self.setMinimumSize(600, 500)
        self.resize(700, 550)
        
        # Apply the dark theme
        ThemeManager.apply_theme(QApplication.instance())
        
        # Set application icon
        self._set_app_icon()
    
    def _set_app_icon(self):
        """Set the application icon from logo file."""
        import sys
        
        # Get the correct path for bundled resources
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        logo_paths = [
            os.path.join(base_path, "resources", "logo.png"),
            os.path.join(base_path, "logo.png"),
            os.path.join(base_path, "assets", "logo.png"),
            "resources/logo.png",  # Fallback for development
            "logo.png",
            "assets/logo.png"
        ]
        
        icon_loaded = False
        for path in logo_paths:
            if os.path.exists(path):
                try:
                    icon = QIcon(path)
                    if not icon.isNull():
                        self.setWindowIcon(icon)
                        # Also set the app icon globally
                        QApplication.instance().setWindowIcon(icon)
                        icon_loaded = True
                        print(f"App icon loaded from: {path}")  # Debug info
                        break
                except Exception as e:
                    print(f"Error loading app icon from {path}: {e}")
                    continue
        
        # If no logo found, create a simple icon
        if not icon_loaded:
            self._create_fallback_icon()
            print("Using fallback app icon")
    
    def _create_fallback_icon(self):
        """Create a fallback icon if no logo is found."""
        from PyQt6.QtGui import QPainter, QBrush, QPen
        from PyQt6.QtCore import QRect
        
        # Create a 32x32 pixmap for the icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw a simple gear/convert icon
        painter.setBrush(QBrush(Qt.GlobalColor.cyan))
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawEllipse(4, 4, 24, 24)
        
        # Draw arrow
        painter.setPen(QPen(Qt.GlobalColor.white, 3))
        painter.drawLine(10, 16, 22, 16)
        painter.drawLine(18, 12, 22, 16)
        painter.drawLine(18, 20, 22, 16)
        
        painter.end()
        
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        QApplication.instance().setWindowIcon(icon)
    
    def setup_ui(self):
        """Setup the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Drag and drop area
        self.drag_drop_area = DragDropArea()
        main_layout.addWidget(self.drag_drop_area)
        
        # File info widget
        self.file_info_widget = FileInfoWidget()
        main_layout.addWidget(self.file_info_widget)
        
        # Conversion options widget
        self.conversion_options_widget = ConversionOptionsWidget()
        main_layout.addWidget(self.conversion_options_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.convert_button = QPushButton("Convert")
        self.convert_button.setEnabled(False)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("secondary")
        
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
    
    def connect_signals(self):
        """Connect signals between view and viewmodel."""
        # Drag and drop
        self.drag_drop_area.file_dropped.connect(self._on_file_dropped)
        
        # Buttons
        self.convert_button.clicked.connect(self._on_convert_clicked)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        
        # Conversion options
        self.conversion_options_widget.options_changed.connect(self._on_options_changed)
        
        # ViewModel signals
        self.viewmodel.file_loaded.connect(self._on_file_loaded)
        self.viewmodel.file_cleared.connect(self._on_file_cleared)
        self.viewmodel.conversion_options_changed.connect(self._on_conversion_options_changed)
        self.viewmodel.conversion_started.connect(self._on_conversion_started)
        self.viewmodel.conversion_progress.connect(self._on_conversion_progress)
        self.viewmodel.conversion_finished.connect(self._on_conversion_finished)
        self.viewmodel.status_message.connect(self._on_status_message)
    
    @pyqtSlot(str)
    def _on_file_dropped(self, file_path: str):
        """Handle file drop or selection."""
        if not file_path:
            # Open file dialog
            file_path = self.viewmodel.select_file()
        
        if file_path:
            self.viewmodel.load_file(file_path)
    
    @pyqtSlot()
    def _on_convert_clicked(self):
        """Handle convert button click."""
        if not self.viewmodel.can_convert():
            return
        
        # Get default output file path (same folder as input)
        default_output_path = self.viewmodel.get_output_filename()
        
        # Ask user if they want to choose a different location
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Save Location")
        msg_box.setText(f"Default save location:\n{default_output_path}\n\nDo you want to choose a different location?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setIcon(QMessageBox.Icon.Question)
        
        # Apply custom styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
                color: #f8fafc;
            }
            QMessageBox QLabel {
                color: #f8fafc;
                background-color: transparent;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e3a8a, 
                    stop:1 #1e40af);
                color: #f8fafc;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, 
                    stop:1 #1e3a8a);
            }
        """)
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            # Let user choose location
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Converted File",
                default_output_path,
                f"Converted Files (*{Path(default_output_path).suffix})"
            )
            if not file_path:
                return  # User cancelled
        else:
            # Use default location
            file_path = default_output_path
        
        self.viewmodel.start_conversion(file_path)
    
    @pyqtSlot()
    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.viewmodel.clear_file()
    
    @pyqtSlot()
    def _on_options_changed(self):
        """Handle conversion options change."""
        if not self.viewmodel.current_file:
            return
        
        # Update viewmodel with current options
        if self.viewmodel.current_file.file_type == FileType.IMAGE:
            options = self.conversion_options_widget.get_image_options()
            if options:
                self.viewmodel.update_image_format(options['format'])
                self.viewmodel.update_image_resize(
                    options['resize_enabled'],
                    options['max_width'],
                    options['max_height']
                )
                self.viewmodel.update_image_size_limit(
                    options['size_limit_enabled'],
                    options['max_size_kb']
                )
        elif self.viewmodel.current_file.file_type == FileType.AUDIO:
            options = self.conversion_options_widget.get_audio_options()
            if options:
                self.viewmodel.update_audio_quality(options['quality'])
        elif self.viewmodel.current_file.file_type == FileType.VIDEO:
            options = self.conversion_options_widget.get_video_options()
            if options:
                self.viewmodel.update_video_quality(options['quality'])
                self.viewmodel.update_video_fast_mode(options['fast_mode'])
    
    @pyqtSlot(object)
    def _on_file_loaded(self, file_info):
        """Handle file loaded signal."""
        self.file_info_widget.update_file_info(file_info)
        self.conversion_options_widget.update_for_file_type(file_info.file_type)
        self.convert_button.setEnabled(True)
        self.drag_drop_area.setVisible(False)
    
    @pyqtSlot()
    def _on_file_cleared(self):
        """Handle file cleared signal."""
        self.file_info_widget.update_file_info(None)
        self.conversion_options_widget.setVisible(False)
        self.convert_button.setEnabled(False)
        self.drag_drop_area.setVisible(True)
        self.progress_bar.setVisible(False)
    
    @pyqtSlot()
    def _on_conversion_options_changed(self):
        """Handle conversion options changed signal."""
        self.convert_button.setEnabled(self.viewmodel.can_convert())
    
    @pyqtSlot()
    def _on_conversion_started(self):
        """Handle conversion started signal."""
        self.convert_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
    
    @pyqtSlot(int)
    def _on_conversion_progress(self, progress: int):
        """Handle conversion progress signal."""
        self.progress_bar.setValue(progress)
    
    @pyqtSlot(bool, str)
    def _on_conversion_finished(self, success: bool, message: str):
        """Handle conversion finished signal."""
        self.convert_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            self._show_message_box("Conversion Complete", f"File converted successfully!\nSaved to: {message}", QMessageBox.Icon.Information)
        else:
            self._show_message_box("Conversion Failed", f"Conversion failed: {message}", QMessageBox.Icon.Critical)
    
    @pyqtSlot(str)
    def _on_status_message(self, message: str):
        """Handle status message signal."""
        self.status_bar.showMessage(message)
    
    def _show_message_box(self, title: str, message: str, icon: QMessageBox.Icon):
        """Show a styled message box."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setIcon(icon)
        
        # Apply custom styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
                color: #f8fafc;
            }
            QMessageBox QLabel {
                color: #f8fafc;
                background-color: transparent;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e3a8a, 
                    stop:1 #1e40af);
                color: #f8fafc;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, 
                    stop:1 #1e3a8a);
            }
        """)
        
        msg_box.exec()
