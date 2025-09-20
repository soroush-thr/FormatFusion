"""
FormatFusion - Universal File Converter
Main application entry point.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from views.main_window import MainWindow


def setup_application():
    """Setup the PyQt6 application."""
    # Enable high DPI scaling (PyQt6 uses different attribute names)
    try:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        # PyQt6 may not have these attributes, continue without them
        pass
    
    app = QApplication(sys.argv)
    app.setApplicationName("FormatFusion")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FormatFusion")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Apply custom dark theme
    from views.main_window import ThemeManager
    ThemeManager.apply_theme(app)
    
    # Set application icon with proper path handling
    def get_logo_path():
        """Get the correct path for the logo file."""
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
        
        for path in logo_paths:
            if os.path.exists(path):
                return path
        return None
    
    logo_path = get_logo_path()
    if logo_path:
        app.setWindowIcon(QIcon(logo_path))
        print(f"App icon set from: {logo_path}")
    else:
        print("No logo found, using default icon")
    
    return app


def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow (PIL)")
    
    try:
        import ffmpeg
    except ImportError:
        missing_deps.append("ffmpeg-python")
    
    if missing_deps:
        error_msg = f"Missing required dependencies:\n{chr(10).join(f'- {dep}' for dep in missing_deps)}\n\n"
        error_msg += "Please install them using:\npip install -r requirements.txt"
        
        QMessageBox.critical(None, "Missing Dependencies", error_msg)
        return False
    
    return True


def check_ffmpeg():
    """Check if FFmpeg is available."""
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=10)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        # Check for bundled ffmpeg.exe
        possible_paths = [
            'ffmpeg.exe',
            'bin/ffmpeg.exe',
            'resources/ffmpeg.exe'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return True
        
        error_msg = "FFmpeg not found!\n\n"
        error_msg += "Please ensure ffmpeg.exe is available in one of these locations:\n"
        error_msg += "- Current directory\n"
        error_msg += "- bin/ directory\n"
        error_msg += "- resources/ directory\n"
        error_msg += "- System PATH\n\n"
        error_msg += "You can download FFmpeg from: https://ffmpeg.org/download.html"
        
        QMessageBox.critical(None, "FFmpeg Not Found", error_msg)
        return False


def main():
    """Main application entry point."""
    # Setup application
    app = setup_application()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check FFmpeg availability
    if not check_ffmpeg():
        sys.exit(1)
    
    # Create and show main window
    try:
        main_window = MainWindow()
        main_window.show()
        
        # Start event loop
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Application Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
