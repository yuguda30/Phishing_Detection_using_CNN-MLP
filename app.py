import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader
from flask import Flask, render_template, request, jsonify
from markdown import markdown
from src.predictor import predict_email_text

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Your actual working paths
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\HP\Downloads\poppler-25.12.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

print("Tesseract exists:", os.path.exists(TESSERACT_PATH))
print("Poppler exists:", os.path.exists(POPPLER_PATH))

PROJECT_DOC_URL = "https://docs.google.com/document/d/1yXjVYXZMqKST87TOMz4ZE8BmBooD1t7U/edit?usp=sharing&ouid=107767377161329712831&rtpof=true&sd=true"
README_URL = "/readme"


def extract_text_with_pymupdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
    except Exception as e:
        print("PyMuPDF extraction failed:", e)
    return text.strip()


def extract_text_with_pypdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print("PyPDF extraction failed:", e)
    return text.strip()


def extract_text_with_ocr(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH, dpi=300)
        for img in images:
            ocr_text = pytesseract.image_to_string(img, lang="eng")
            text += ocr_text + "\n"
    except Exception as e:
        print("OCR extraction failed:", e)
    return text.strip()


def extract_text_from_pdf(pdf_path):
    # 1. Try PyMuPDF
    extracted_text = extract_text_with_pymupdf(pdf_path)
    if extracted_text:
        return extracted_text, "pymupdf"

    # 2. Try PyPDF
    extracted_text = extract_text_with_pypdf(pdf_path)
    if extracted_text:
        return extracted_text, "pypdf"

    # 3. OCR fallback
    extracted_text = extract_text_with_ocr(pdf_path)
    if extracted_text:
        return extracted_text, "ocr"

    return "", "none"


@app.route("/")
def home():
    return render_template(
        "index.html",
        project_doc_url=PROJECT_DOC_URL,
        readme_url=README_URL
    )


@app.route("/predict-text", methods=["POST"])
def predict_text():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data received."}), 400

    email_text = data.get("email_text", "").strip()

    if not email_text:
        return jsonify({"error": "Please paste an email message."}), 400

    result = predict_email_text(email_text)
    result["input_type"] = "text"

    return jsonify(result), 200


@app.route("/predict-pdf", methods=["POST"])
def predict_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "No PDF file uploaded."}), 400

    file = request.files["pdf_file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed."}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    extracted_text, method_used = extract_text_from_pdf(file_path)

    if not extracted_text.strip():
        return jsonify({
            "error": "No readable text found in the PDF. The file may be image-based, scanned, or unreadable."
        }), 400

    result = predict_email_text(extracted_text)
    result["input_type"] = "pdf"
    result["extracted_text_preview"] = extracted_text[:1500]
    result["extraction_method"] = method_used

    return jsonify(result), 200


@app.route("/readme")
def readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        return f"<html><body style='font-family:Arial;padding:30px;'>{markdown(content)}</body></html>"

    return "README.md not found.", 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)