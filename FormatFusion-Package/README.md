# FormatFusion - Universal File Converter

A modern, high-performance desktop application for Windows that converts images, audio, and video files with an intuitive drag-and-drop interface. Built with Python and PyQt6 following the MVVM design pattern, featuring a beautiful dark theme and optimized conversion engines.

## ✨ Key Features

### 🖼️ **Advanced Image Conversion**
- **Supported Input Formats**: PNG, JPG, JPEG, BMP, TIFF, GIF, WebP
- **Output Formats**: PNG, JPG with quality optimization
- **Smart Resizing**: Optional pixel-based resizing with aspect ratio preservation
- **File Size Control**: Kilobyte-based size limiting with intelligent compression
- **Quality Engine**: High-quality conversion using Pillow with optimization algorithms

### 🎵 **Professional Audio Conversion**
- **Supported Input Formats**: WAV, M4A, FLAC, OGG, MP3, AAC, WMA
- **Output Format**: MP3 with optimized encoding
- **Quality Presets**: 128kbps (Standard), 192kbps (Good), 256kbps (High), 320kbps (Lossless)
- **Fast Processing**: Optimized FFmpeg integration

### 🎬 **Ultra-Fast Video Conversion**
- **Supported Input Formats**: MKV, MOV, AVI, WebM, FLV, MP4, WMV, M4V
- **Output Format**: MP4 with H.264/AAC codecs
- **Quality Presets**: 480p, 720p, 1080p, Original quality
- **Speed Optimization**: 3-5x faster conversion with hardware acceleration
- **Fast Mode**: Ultrafast encoding for maximum speed
- **Hardware Acceleration**: Auto-detects NVIDIA, Intel, and AMD GPU encoding

### 🎨 **Modern User Interface**
- **Dark Theme**: Professional navy-blue color scheme
- **Drag & Drop**: Intuitive file selection with visual feedback
- **Real-time Preview**: File information and conversion options
- **Progress Tracking**: Visual progress bar with real-time updates
- **Smart Defaults**: Automatic save location in same folder as input
- **Error Handling**: Clear error messages and validation
- **Logo Support**: Custom logo integration throughout the interface

## Installation

### Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **FFmpeg**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract and place `ffmpeg.exe` in one of these locations:
     - Project root directory
     - `bin/` directory
     - `resources/` directory
     - System PATH

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd FormatFusion
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify FFmpeg Installation**
   - Place `ffmpeg.exe` in the project root directory
   - Or ensure it's available in your system PATH

## Running the Application

### From Source Code
```bash
python main.py
```

### First Run
1. Launch the application
2. Drag and drop a file onto the main area, or click to browse
3. Select your conversion options
4. Click "Convert" and choose output location
5. Wait for conversion to complete

## Building Executable

### Using PyInstaller

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create Executable**
   ```bash
   pyinstaller --onefile --windowed --name FormatFusion main.py
   ```

3. **Include FFmpeg**
   ```bash
   pyinstaller --onefile --windowed --name FormatFusion --add-data "ffmpeg.exe;." main.py
   ```

### Advanced Build Script
Create `build.py` for automated building:

```python
import PyInstaller.__main__
import os

# Build executable
PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--name=FormatFusion',
    '--add-data=ffmpeg.exe;.',
    '--add-data=requirements.txt;.',
    '--icon=icon.ico',  # Optional: add custom icon
    'main.py'
])
```

## 📁 Project Structure

```
FormatFusion/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── setup.py                   # Automated setup script
├── build.py                   # Executable build script
├── README.md                  # This documentation
├── ffmpeg.exe                 # FFmpeg binary (place here)
├── resources/                 # Application resources
│   ├── logo.png              # Custom logo (optional)
│   └── README.md             # Logo setup instructions
├── temp/                     # Documentation and guides
│   ├── SETUP_GUIDE.md        # Simple setup guide
│   └── VIDEO_OPTIMIZATION.md # Performance details
├── models/                   # Data models (MVVM)
│   ├── __init__.py
│   ├── file_info.py          # File information model
│   └── conversion_options.py # Conversion settings model
├── viewmodels/               # Business logic (MVVM)
│   ├── __init__.py
│   └── main_viewmodel.py     # Main view model
├── views/                    # User interface (MVVM)
│   ├── __init__.py
│   └── main_window.py        # Main window with dark theme
├── services/                 # External services
│   ├── __init__.py
│   └── conversion_service.py # Optimized conversion engine
└── utils/                    # Utility functions
    ├── __init__.py
    └── file_utils.py         # File operation utilities
```

## 🚀 Performance Optimizations

### **Video Conversion Speed**
- **3-5x Faster**: Optimized FFmpeg settings with ultrafast presets
- **Hardware Acceleration**: Auto-detects and uses GPU encoding (NVIDIA, Intel, AMD)
- **Fast Mode**: Default setting for maximum speed with minimal quality loss
- **Smart Fallbacks**: Automatic fallback to software encoding if hardware fails

### **Image Processing**
- **Intelligent Compression**: Smart quality adjustment for file size limits
- **Memory Efficient**: Optimized Pillow usage with proper resource management
- **Batch Processing**: Efficient handling of multiple image operations

### **Audio Conversion**
- **Optimized Encoding**: Fast MP3 conversion with quality presets
- **Stream Processing**: Efficient audio stream handling

## 🎨 User Experience

### **Modern Interface**
- **Dark Theme**: Professional navy-blue color scheme with cyan accents
- **Responsive Design**: Adapts to different window sizes
- **Visual Feedback**: Hover effects, progress bars, and status updates
- **Custom Logo**: Support for custom branding throughout the interface

### **Smart Features**
- **Auto Save Location**: Defaults to same folder as input file
- **File Type Detection**: Automatic format recognition and appropriate options
- **Progress Tracking**: Real-time conversion progress with visual indicators
- **Error Recovery**: Graceful error handling with helpful messages

## 🏗️ Architecture

FormatFusion follows the **Model-View-ViewModel (MVVM)** pattern:

- **Models**: Data structures and business entities (`file_info.py`, `conversion_options.py`)
- **Views**: User interface components (`main_window.py` with dark theme)
- **ViewModels**: Business logic and state management (`main_viewmodel.py`)
- **Services**: External dependencies and conversion logic (`conversion_service.py`)
- **Utils**: Helper functions and utilities (`file_utils.py`)

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" Error**
   - Ensure `ffmpeg.exe` is in the correct location
   - Check that the file is not corrupted
   - Verify FFmpeg works from command line: `ffmpeg -version`

2. **"Missing Dependencies" Error**
   - Run `pip install -r requirements.txt`
   - Ensure you're using the correct Python version
   - Try creating a fresh virtual environment

3. **Conversion Fails**
   - Check that input file is not corrupted
   - Ensure output directory is writable
   - Verify file format is supported

4. **Application Won't Start**
   - Check Python version (3.8+ required)
   - Verify all dependencies are installed
   - Check for antivirus interference

### Performance Tips

- For large video files, use "Original" quality to avoid re-encoding
- Close other applications during conversion for better performance
- Use SSD storage for faster file I/O

## Development

### Adding New File Formats

1. Update `FileType` enum in `models/file_info.py`
2. Add extension mapping in `_detect_file_type()` method
3. Implement conversion logic in `services/conversion_service.py`
4. Add UI options in `views/main_window.py`

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Image, audio, and video conversion
- Drag-and-drop interface
- MVVM architecture
- Windows executable support