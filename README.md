# Text File Splitter
A modern PyQt5 application for splitting text files into multiple parts.

## Features
- 🎨 Modern, beautiful UI with gradient backgrounds
- 📁 Drag and drop file support
- 📊 Progress bar for large files
- 🎯 Custom output directory selection
- 👀 File preview functionality
- 🌙 Dark/Light theme toggle
- 💾 Settings persistence
- 🔄 Batch processing (split multiple files at once)
- ⚙️ Configurable number of output files

## Installation

### From Source
1. Clone the repository:
```bash
git clone https://github.com/starsigns/textssplitter.git
cd textssplitter
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install PyQt5
```

5. Run the application:
```bash
python text_splitter_app.py
```

### Standalone Executable
Download the standalone executable from the releases page - no Python installation required!

## Usage
1. **Select Files**: Click "Browse Files" or drag and drop text files into the application
2. **Choose Output**: Select where you want the split files to be saved
3. **Set Split Count**: Choose how many files you want each text file split into
4. **Split**: Click the "Split Files" button to process your files
5. **Preview**: Select any file from the list to preview its contents

## Building from Source
To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico --name="TextFileSplitter" text_splitter_app.py
```

## Requirements
- Python 3.7+
- PyQt5

## License
MIT License - feel free to use and modify as needed.

## Contributing
Pull requests and issues are welcome!
