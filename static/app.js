function showLoading(message = "Analyzing...") {
  const loadingCard = document.getElementById("loadingCard");
  loadingCard.classList.remove("hidden");
  document.getElementById("loadingText").textContent = message;

  document.getElementById("resultCard").classList.add("hidden");
  document.getElementById("errorCard").classList.add("hidden");

  loadingCard.scrollIntoView({ behavior: "smooth", block: "center" });
}

function hideLoading() {
  document.getElementById("loadingCard").classList.add("hidden");
}

function showError(message) {
  hideLoading();
  document.getElementById("errorMessage").textContent = message;
  document.getElementById("errorCard").classList.remove("hidden");
  document.getElementById("errorCard").scrollIntoView({ behavior: "smooth", block: "center" });
}

function showResult(data, isPdf = false) {
  hideLoading();

  const badge = document.getElementById("resultBadge");
  badge.className = data.label === "Phishing" ? "result-phishing" : "result-legitimate";
  badge.textContent = `Result: ${data.label}`;

  document.getElementById("confidence").textContent = data.confidence;
  document.getElementById("probability").textContent = data.probability;
  document.getElementById("riskLevel").textContent = data.risk_status;
  document.getElementById("confidenceLevel").textContent = data.confidence_level;
  document.getElementById("summary").textContent = data.summary;
  document.getElementById("processedText").textContent = data.processed_text;

  const pdfPreviewBox = document.getElementById("pdfPreviewBox");
  const pdfPreview = document.getElementById("pdfPreview");

  if (isPdf && data.extracted_text_preview) {
    pdfPreviewBox.classList.remove("hidden");
    pdfPreview.textContent = data.extracted_text_preview;
  } else {
    pdfPreviewBox.classList.add("hidden");
    pdfPreview.textContent = "";
  }

  document.getElementById("resultCard").classList.remove("hidden");
  document.getElementById("resultCard").scrollIntoView({ behavior: "smooth", block: "start" });
}

async function submitText() {
  const emailText = document.getElementById("emailText").value.trim();

  if (!emailText) {
    showError("Please paste an email message.");
    return;
  }

  showLoading("Extracting and analyzing email text...");

  try {
    const response = await fetch("/predict-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email_text: emailText })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");

    showResult(data, false);
  } catch (error) {
    showError(error.message);
  }
}

async function submitPDF() {
  const fileInput = document.getElementById("pdfFile");
  const file = fileInput.files[0];

  if (!file) {
    showError("Please select a PDF file.");
    return;
  }

  const formData = new FormData();
  formData.append("pdf_file", file);

  showLoading("Extracting text from PDF and analyzing...");

  try {
    const response = await fetch("/predict-pdf", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "PDF analysis failed.");

    showResult(data, true);
  } catch (error) {
    showError(error.message);
  }
}

document.getElementById("summary").textContent =
  data.summary + (data.extraction_method ? ` Extraction method: ${data.extraction_method.toUpperCase()}.` : "");