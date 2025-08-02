# 🔧 CysawTool

> \[!NOTE]
> On the Cysaw Discord, they say:
> *“Do not try to bypass ads or use automated tools. This may result in temporary access restrictions. Please use the website normally through your browser.”*
>
> The reality is they **can’t detect** this tool — it’s highly advanced and designed to avoid detection. So don’t worry, you won’t get banned from the website.
> And if Cysaw releases an update, the tool will be updated within 30 minutes! (Or much if its by night, my time code: https://time.is/Paris)


## 🤡
![clown](image.png)
---

Message to Cysaw:
Obfuscate the code bruh i have access to all security patches

**CysawTool** is a Python tool that automatically downloads applications from cysaw.org by bypassing ShrinkMe protected links.

## ✨ Features

* 🎯 Automatic retrieval of download links via the cysaw\.org API
* 🔓 Automated bypass of ShrinkMe protections
* 📦 Automatic download and extraction of ZIP archives
* 🎨 Colorful and intuitive command-line interface
* ⚡ Fast and efficient processing

## 📋 Requirements

* Python 3.7+
* pip (Python package manager)

## 🚀 Installation

### Automatic installation (Windows)

```bash
git clone https://github.com/VapRtool/CysawTool.git
cd CysawTool
setup.bat
```

### Manual installation

```bash
git clone https://github.com/VapRtool/CysawTool.git
cd CysawTool
pip install -r requirements.txt
```

## 🎮 Usage

### Quick start (Windows)

```bash
start.bat
```

### Manual launch

```bash
python main.py
```

1. Run the script
2. Enter the **AppID** of the application you want to download
3. Wait while the tool automatically processes the download
4. The archive will be extracted into a folder with the same name

## 📝 Usage example

```
┌───(COMPUTER)
└──$ Enter AppID: 431960
└──$ Processing protected link...
└──$ Waiting for bypass timer...
└──$ Downloading and extracting file...
└──$ Downloaded: 431960.zip
└──$ Extracted to: 431960
└──$ Cleaned up: 431960.zip
```

## 📦 Dependencies

* `requests` - HTTP requests
* `cloudscraper` - Anti-bot protection bypass
* `beautifulsoup4` - HTML parsing
* `pystyle` - Terminal colors and styles

## ⚙️ Project structure

```
CysawTool/
├── main.py           # Main script
├── requirements.txt   # Python dependencies
├── setup.bat          # Automatic installation
├── start.bat          # Quick launch
└── README.md          # Documentation
```

## 🛠️ Technical workflow

1. **Link retrieval**: The tool uses the cysaw\.org API to get the ShrinkMe link
2. **Bypass**: Simulates a browser to bypass the timer protection
3. **Download**: Retrieves the file from the direct link obtained
4. **Extraction**: Automatically decompresses the ZIP archive

## ⚠️ Warning

This tool is intended for educational and personal use only. The user is responsible for their usage and must comply with the terms of service of the sites involved.

## 🐛 Known issues

* Wait times are necessary to bypass anti-bot protections
* Some links may not work depending on the server configuration

## 🤝 Contribution

Contributions are welcome! Feel free to:

* Report bugs
* Suggest improvements
* Submit pull requests

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

⭐ **Don’t forget to star the project if it was useful to you!**
