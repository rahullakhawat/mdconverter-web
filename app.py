from flask import Flask, request, render_template, send_file
from markitdown import MarkItDown
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["input_file"]
    output_filename = request.form["output_filename"]

    # Save uploaded file temporarily
    temp_input = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_input)

    # Convert to markdown
    md = MarkItDown()
    result = md.convert(temp_input)

    # Save output temporarily
    temp_output = os.path.join(UPLOAD_FOLDER, output_filename + ".md")
    with open(temp_output, "w", encoding="utf-8") as f:
        f.write(result.text_content)

    # Clean up input file
    os.remove(temp_input)

    # Send the .md file as a download to the user
    return send_file(temp_output, as_attachment=True, download_name=output_filename + ".md")

if __name__ == "__main__":
    app.run(debug=True)
