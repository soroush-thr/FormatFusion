"""
Build script for FormatFusion executable.
Creates a standalone executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_ffmpeg():
    """Check if FFmpeg is available."""
    ffmpeg_paths = [
        'ffmpeg.exe',
        'bin/ffmpeg.exe',
        'resources/ffmpeg.exe'
    ]
    
    for path in ffmpeg_paths:
        if os.path.exists(path):
            print(f"✓ Found FFmpeg at: {path}")
            return path
    
    print("✗ FFmpeg not found!")
    print("Please download ffmpeg.exe and place it in the project root directory.")
    print("Download from: https://ffmpeg.org/download.html")
    return None


def install_pyinstaller():
    """Install PyInstaller if not available."""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False


def build_executable():
    """Build the executable using PyInstaller."""
    print("Building FormatFusion executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=FormatFusion',
        '--clean',
        '--noconfirm'
    ]
    
    # Add FFmpeg if found
    ffmpeg_path = check_ffmpeg()
    if ffmpeg_path:
        cmd.extend(['--add-data', f'{ffmpeg_path};.'])
    
    # Add logo if found
    logo_paths = ['resources/logo.png', 'logo.png', 'assets/logo.png']
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            cmd.extend(['--add-data', f'{logo_path};resources'])
            break
    
    # Add main script
    cmd.append('main.py')
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        print("✓ Output: dist/FormatFusion.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False


def create_distribution():
    """Create distribution package."""
    print("Creating distribution package...")
    
    dist_dir = Path('dist')
    package_dir = Path('FormatFusion-Package')
    
    # Create package directory
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    exe_path = dist_dir / 'FormatFusion.exe'
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir)
        print("✓ Copied executable")
    
    # Copy FFmpeg if not bundled
    ffmpeg_path = check_ffmpeg()
    if ffmpeg_path and not ffmpeg_path.startswith('dist'):
        shutil.copy2(ffmpeg_path, package_dir)
        print("✓ Copied FFmpeg")
    
    # Copy README
    if os.path.exists('README.md'):
        shutil.copy2('README.md', package_dir)
        print("✓ Copied README")
    
    # Create batch file for easy launch
    batch_content = """@echo off
echo Starting FormatFusion...
FormatFusion.exe
pause
"""
    with open(package_dir / 'Run-FormatFusion.bat', 'w') as f:
        f.write(batch_content)
    print("✓ Created launcher batch file")
    
    print(f"✓ Distribution package created: {package_dir}")
    return True


def main():
    """Main build process."""
    print("FormatFusion Build Script")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Build executable
    if not build_executable():
        return False
    
    # Create distribution
    if not create_distribution():
        return False
    
    print("\n" + "=" * 30)
    print("Build completed successfully!")
    print("Distribution package: FormatFusion-Package/")
    print("Executable: dist/FormatFusion.exe")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
