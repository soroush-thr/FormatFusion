# FormatFusion Setup Guide

A simple guide to get FormatFusion running and create an executable app.

## 🚀 Quick Start

### Step 1: Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation
- Verify installation: Open Command Prompt and type `python --version`

### Step 2: Create Virtual Environment
Open Command Prompt in the FormatFusion folder and run:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```
You should see `(venv)` at the beginning of your command prompt.

### Step 3: Download FFmpeg
- Go to [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Download the Windows build (static version)
- Extract the ZIP file
- Copy `ffmpeg.exe` to your FormatFusion project folder

### Step 4: Install Dependencies
With your virtual environment activated, run:
```bash
python setup.py
```
This will automatically install all required Python packages.

### Step 5: Add Your Logo (Optional)
1. Create a logo image (PNG format, transparent background)
2. Name it `logo.png`
3. Place it in the `resources/` folder
4. Recommended size: 64x64 or 128x128 pixels
5. The app will automatically use your logo in:
   - The main drag-and-drop area
   - Window title bar icon
   - All dialog boxes

### Step 6: Run the Application
```bash
python main.py
```

## 📦 Creating an Executable

### Method 1: Using the Build Script (Recommended)
Make sure your virtual environment is activated, then run:
```bash
python build.py
```
This creates a `FormatFusion-Package` folder with everything you need.

### Method 2: Manual PyInstaller
With virtual environment activated:
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name FormatFusion --add-data "ffmpeg.exe;." main.py
```

## 🔧 Troubleshooting

### "Python not found"
- Make sure Python is installed and added to PATH
- Try using `python3` instead of `python`

### "FFmpeg not found"
- Download FFmpeg from the official website
- Place `ffmpeg.exe` in the same folder as `main.py`
- Or put it in a `bin/` or `resources/` folder

### "Module not found" errors
- Make sure your virtual environment is activated (you should see `(venv)` in your prompt)
- Run `pip install -r requirements.txt`
- Make sure you're in the correct directory

### Application won't start
- Check that all files are in the right place
- Make sure FFmpeg is in the project folder
- Try running `python test_app.py` to check dependencies

## 📁 File Structure
Make sure your project looks like this:
```
FormatFusion/
├── main.py
├── ffmpeg.exe          ← Important!
├── requirements.txt
├── setup.py
├── build.py
├── resources/
│   └── logo.png        ← Optional: Your logo file
├── models/
├── viewmodels/
├── views/
├── services/
└── utils/
```

## 🎨 Adding Your Logo (Optional)
1. Create a logo image (PNG format, transparent background)
2. Name it `logo.png`
3. Place it in the `resources/` folder
4. Recommended size: 64x64 or 128x128 pixels
5. The app will automatically use your logo in:
   - The main drag-and-drop area
   - Window title bar icon
   - All dialog boxes

## 🎯 What You Get

After building, you'll have:
- **FormatFusion.exe** - The main application
- **ffmpeg.exe** - Required for audio/video conversion
- **Run-FormatFusion.bat** - Easy launcher

## ✨ New Features

### **Ultra-Fast Video Conversion**
- **3-5x Faster**: Optimized settings for maximum speed
- **Hardware Acceleration**: Auto-detects GPU encoding
- **Fast Mode**: Enabled by default for best performance
- **Smart Fallbacks**: Automatic error recovery

### **Advanced Image Processing**
- **File Size Control**: Set maximum file size in KB
- **Smart Compression**: Automatic quality adjustment
- **Resize Options**: Pixel-based resizing with aspect ratio preservation

### **Professional Interface**
- **Dark Theme**: Beautiful navy-blue color scheme
- **Custom Logo**: Add your own branding
- **Smart Defaults**: Saves to same folder as input
- **Progress Tracking**: Real-time conversion progress

## 💡 Tips

1. **First Time Setup**: Always run `python setup.py` first
2. **FFmpeg Location**: Keep `ffmpeg.exe` in the same folder as the app
3. **Video Conversion**: Enable "Fast Mode" for best speed
4. **File Sizes**: Large video files convert much faster now
5. **Output Folder**: Defaults to same folder as input file
6. **Logo**: Add `logo.png` to `resources/` folder for custom branding

## 🆘 Need Help?

1. Check the main README.md for detailed information
2. Run `python test_app.py` to test if everything works
3. Make sure all files are in the correct locations
4. Verify Python and FFmpeg are properly installed

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] FFmpeg downloaded and placed in project folder
- [ ] Dependencies installed (`python setup.py`)
- [ ] Application runs (`python main.py`)
- [ ] Executable created (`python build.py`)

That's it! You should now have a working FormatFusion application. 🎉
