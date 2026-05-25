# Build Smart Trash Downloader EXE

## 📋 Requirements

- Python 3.10+ (already installed)
- PyInstaller: `pip install pyinstaller>=6.0.0`

## 🛠️ Build the EXE

### Method 1: Using spec file (Recommended)

```powershell
cd SmartTrash
pyinstaller SmartTrashDownloader.spec
```

EXE location: `dist/SmartTrashDownloader.exe`

### Method 2: Command line (One-liner)

```powershell
pyinstaller --noconfirm --windowed --name SmartTrashDownloader downloader.py
```

### Method 3: One-file EXE (all in 1 file)

```powershell
pyinstaller --noconfirm --onefile --windowed --name SmartTrashDownloader downloader.py
```

## 📦 Build Output

```
dist/
├── SmartTrashDownloader.exe      (Main executable)
└── (supporting libraries)
```

## ✨ Downloader Features

✅ Modern GUI interface
✅ Auto-create folder structure (model/, assets/, Arduino/)
✅ Install all Python dependencies
✅ Show progress bar
✅ Detailed installation logs
✅ Friendly error handling
✅ Vietnamese UI

## 🎯 How Users Use It

1. Run `SmartTrashDownloader.exe`
2. Choose installation folder (default: `C:\Users\YourName\SmartTrash`)
3. Click "🚀 Bắt đầu cài đặt" (Start Installation)
4. Wait for packages to install (5-15 minutes first time)
5. When complete, add `keras_model.h5` to the `model/` folder
6. Run `python app.py`

## 📝 Notes

- First run installs TensorFlow (~500MB, takes time)
- Requires internet connection
- Installation takes 5-15 minutes depending on internet speed

## 🔧 Troubleshooting

**Error "Could not find pip":**
```powershell
python -m pip install --upgrade pip
```

**Build fails:**
```powershell
pip install --upgrade pyinstaller
pyinstaller --clean SmartTrashDownloader.spec
```

**EXE won't start:**
Run from command line to see details:
```powershell
SmartTrashDownloader.exe
```

## 🚀 Quick Start

```powershell
# Install PyInstaller
pip install pyinstaller

# Build EXE
pyinstaller SmartTrashDownloader.spec

# Run the downloader
dist/SmartTrashDownloader.exe
```

Done! 🎉
