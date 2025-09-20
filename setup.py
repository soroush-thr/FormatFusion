"""
Setup script for FormatFusion.
Installs dependencies and sets up the environment.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def check_ffmpeg():
    """Check if FFmpeg is available."""
    print("Checking for FFmpeg...")
    
    # Check if ffmpeg is in PATH
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=10)
        print("✓ FFmpeg found in system PATH")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check for bundled ffmpeg.exe
    possible_paths = [
        'ffmpeg.exe',
        'bin/ffmpeg.exe',
        'resources/ffmpeg.exe'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found FFmpeg at: {path}")
            return True
    
    print("✗ FFmpeg not found!")
    print("\nPlease download FFmpeg:")
    print("1. Go to https://ffmpeg.org/download.html")
    print("2. Download the Windows build")
    print("3. Extract ffmpeg.exe to this directory")
    print("4. Run this setup script again")
    
    return False


def create_directories():
    """Create necessary directories."""
    directories = ['bin', 'resources', 'icons', 'dist']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def create_launcher_script():
    """Create a launcher script for easy execution."""
    if platform.system() == "Windows":
        launcher_content = """@echo off
echo Starting FormatFusion...
python main.py
pause
"""
        with open('run_formatfusion.bat', 'w') as f:
            f.write(launcher_content)
        print("✓ Created launcher script: run_formatfusion.bat")
    else:
        launcher_content = """#!/bin/bash
echo "Starting FormatFusion..."
python3 main.py
"""
        with open('run_formatfusion.sh', 'w') as f:
            f.write(launcher_content)
        os.chmod('run_formatfusion.sh', 0o755)
        print("✓ Created launcher script: run_formatfusion.sh")


def main():
    """Main setup process."""
    print("FormatFusion Setup")
    print("=" * 20)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check FFmpeg
    ffmpeg_available = check_ffmpeg()
    
    # Create launcher script
    create_launcher_script()
    
    print("\n" + "=" * 20)
    if ffmpeg_available:
        print("Setup completed successfully!")
        print("\nTo run the application:")
        if platform.system() == "Windows":
            print("  Double-click run_formatfusion.bat")
            print("  OR run: python main.py")
        else:
            print("  Run: ./run_formatfusion.sh")
            print("  OR run: python3 main.py")
    else:
        print("Setup completed with warnings!")
        print("Please install FFmpeg and run this script again.")
    
    return ffmpeg_available


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
