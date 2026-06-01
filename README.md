# MDConverter Web 🗂️➡️📝

A free, open-source web app to convert documents and files into Markdown (`.md`) format — powered by [Microsoft's MarkItDown](https://github.com/microsoft/markitdown) library.

Upload your file, give it a name, and download the converted Markdown instantly. No sign-up. No cost. No hassle. **Your files are deleted from the server immediately after conversion.**

---

## 🌐 Live App

👉 **[Try it here](https://mdconverter-web-production.up.railway.app)**

---

## ✨ Features

- **Single file conversion** — upload one file, download a `.md` file instantly
- **Batch conversion** — upload multiple files, download them all as a `.zip`
- **REST API** — free API for developers, no key required
- **Privacy first** — files are deleted from the server immediately after conversion
- **No sign-up** — just upload and convert
- **Open source** — powered by Microsoft MarkItDown

---

## ✅ Supported File Types

| Category | Formats |
|---|---|
| Microsoft Office | `.docx`, `.xlsx`, `.xls`, `.pptx` |
| PDF | `.pdf` |
| Images | `.jpg`, `.jpeg`, `.png` |
| Audio | `.mp3`, `.wav` |
| Web | `.html` |
| Data | `.csv`, `.json`, `.xml` |
| Archives | `.zip` |

---

## 🚀 How to Use

**Single file:**
1. Go to the live app
2. Click **Browse** and select your file
3. Enter a name for the output file
4. Click **Convert & Download** — your `.md` file downloads automatically

**Batch conversion:**
1. Select multiple files at once
2. Click **Convert & Download** — all files are converted and downloaded as a `.zip`

---

## 🔌 API for Developers

Free REST API — no API key required.

**Convert a file:**
```bash
curl -X POST https://mdconverter-web-production.up.railway.app/api/convert \
  -F "file=@yourfile.pdf"
```

**Python example:**
```python
import requests

with open("myfile.pdf", "rb") as f:
    response = requests.post(
        "https://mdconverter-web-production.up.railway.app/api/convert",
        files={"file": f}
    )

data = response.json()
print(data["markdown"])
```

**Response format:**
```json
{
  "success": true,
  "filename": "yourfile.pdf",
  "markdown": "# Your converted content here..."
}
```

**Full API docs endpoint:**
```
GET https://mdconverter-web-production.up.railway.app/api/docs
```

---

## 🔒 Privacy

- Files are deleted from the server **immediately** after conversion
- We do not store, log, or share any uploaded documents
- The app is open source — you can verify this yourself

---

## 🛠️ Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/mdconverter-web.git
cd mdconverter-web
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python app.py
```

**4. Open in your browser**
```
http://localhost:5000
```

---

## 🧰 Built With

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- Deployed on [Railway](https://railway.app)

---

## 👤 Author

**Rahul Lakhawat**
- GitHub: [@yourusername](https://github.com/yourusername)

---

## ⭐ Support

If you find this tool useful, please consider giving it a **star on GitHub** — it helps others discover it!

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
