from flask import Flask, request, render_template, send_file, jsonify
from markitdown import MarkItDown
import os
import zipfile
import fitz

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.jpg', '.jpeg', '.png', '.html', '.csv', '.json', '.xml', '.zip', '.mp3', '.wav'}

import fitz  # pymupdf

def is_scanned_pdf(filepath):
    """Check if a PDF is scanned (has no extractable text)"""
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        # If less than 50 characters extracted, it's likely a scanned PDF
        return len(text.strip()) < 50
    except:
        return False

def convert_file(file, output_filename):
    temp_input = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_input)

    # Check if it's a scanned PDF and run OCR if needed
    ext = os.path.splitext(file.filename)[1].lower()
    if ext == ".pdf" and is_scanned_pdf(temp_input):
        ocr_output = temp_input.replace(".pdf", "_ocr.pdf")
        try:
            import ocrmypdf
            ocrmypdf.ocr(temp_input, ocr_output, skip_text=True)
            os.remove(temp_input)
            temp_input = ocr_output
        except Exception as e:
            print(f"OCR failed, trying without OCR: {e}")

    md = MarkItDown()
    result = md.convert(temp_input)
    os.remove(temp_input)
    return result.text_content

# -----------------------------------------------
# WEBPAGE ROUTES
# -----------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("input_files")
    if not files:
        return render_template("index.html", error="No files uploaded.")

    # Single file — download directly
    if len(files) == 1:
        file = files[0]
        output_filename = request.form.get("output_filename", "output")
        content = convert_file(file, output_filename)
        temp_output = os.path.join(UPLOAD_FOLDER, output_filename + ".md")
        with open(temp_output, "w", encoding="utf-8") as f:
            f.write(content)
        response = send_file(temp_output, as_attachment=True, download_name=output_filename + ".md")

        @response.call_on_close
        def cleanup_single():
            if os.path.exists(temp_output):
                os.remove(temp_output)

        return response

    # Multiple files — zip them all
    zip_path = os.path.join(UPLOAD_FOLDER, "converted_files.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in files:
            name = os.path.splitext(file.filename)[0]
            content = convert_file(file, name)
            md_filename = name + ".md"
            md_path = os.path.join(UPLOAD_FOLDER, md_filename)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(content)
            zipf.write(md_path, md_filename)
            os.remove(md_path)

    response = send_file(zip_path, as_attachment=True, download_name="converted_files.zip")

    @response.call_on_close
    def cleanup_zip():
        if os.path.exists(zip_path):
            os.remove(zip_path)

    return response


# -----------------------------------------------
# API ROUTES
# -----------------------------------------------

@app.route("/api/convert", methods=["POST"])
def api_convert():
    if "file" not in request.files:
        return jsonify({"error": "No file provided. Send a file using form key 'file'."}), 400

    file = request.files["file"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": f"Unsupported file type: {ext}"}), 400

    try:
        content = convert_file(file, file.filename)
        return jsonify({
            "success": True,
            "filename": file.filename,
            "markdown": content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/docs", methods=["GET"])
def api_docs():
    return jsonify({
        "name": "MDConverter API",
        "version": "1.0",
        "description": "Convert documents to Markdown format",
        "endpoints": {
            "POST /api/convert": {
                "description": "Convert a single file to Markdown",
                "parameters": {
                    "file": "The file to convert (multipart/form-data)"
                },
                "supported_formats": list(ALLOWED_EXTENSIONS),
                "returns": {
                    "success": "true/false",
                    "filename": "original filename",
                    "markdown": "converted markdown text"
                },
                "examples": {
                    "python": "import requests\nwith open('file.pdf', 'rb') as f:\n    r = requests.post('https://your-url/api/convert', files={'file': f})\nprint(r.json()['markdown'])",
                    "curl": "curl -X POST https://your-url/api/convert -F 'file=@yourfile.pdf'"
                }
            }
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
