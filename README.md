# MailSentinel AI

**Intelligent Phishing Email Detection using a Hybrid CNN–MLP Deep Learning Model**

MailSentinel AI is a phishing email detection system that uses a hybrid **Convolutional Neural Network (CNN)** and **Multilayer Perceptron (MLP)** model to classify email content as **Phishing** or **Legitimate**. The system supports both **pasted email text** and **PDF email upload**, with OCR fallback for image-based PDFs.



## Project Highlights

- Hybrid **CNN–MLP** phishing detection model
- Web-based interface built with **Flask**
- Supports:
  - pasted email text
  - uploaded PDF email files
- OCR support for scanned or image-based PDFs
- Displays:
  - prediction result
  - confidence score
  - confidence level
  - risk status
  - processed text preview



## Model Performance

The trained model achieved strong classification performance:

- **Accuracy:** ~98.5%
- **Precision:** ~98.0%
- **Recall:** ~99.1%
- **F1-score:** ~98.6%

These results indicate that the model is highly effective in detecting phishing emails while maintaining a low false-negative rate.



## System Workflow

1. Data acquisition from Kaggle dataset
2. Text preprocessing
3. Tokenization and padding
4. Feature extraction using CNN
5. Classification using MLP
6. Model evaluation
7. Web-based prediction interface



## Project Structure

MyProject/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   └── phishing_email.csv
│
├── models/
│   ├── best_phishing_cnn_mlp.keras
│   ├── final_phishing_cnn_mlp.keras
│   ├── tokenizer.pkl
│   ├── model_config.json
│   ├── X_train.npy
│   ├── X_test.npy
│   ├── y_train.npy
│   └── y_test.npy
│
├── outputs/
│   ├── accuracy_plot.png
│   ├── loss_plot.png
│   ├── class_distribution.png
│   ├── confusion_matrix.png
│   └── training_history.json
│
├── src/
│   ├── 01_load_data.py
│   ├── 02_preprocess.py
│   ├── 03_tokenize_split.py
│   ├── 04_build_train_model.py
│   ├── 05_evaluate_model.py
│   ├── 06_predict_email.py
│   ├── 07_plot_class_distribution.py
│   ├── 08_plot_loss_curve.py
│   ├── predictor.py
│   └── utils.py
│
├── static/
│   ├── app.js
│   └── style.css
│
├── templates/
│   └── index.html
│
└── uploads/


## Technologies Used
Python
TensorFlow / Keras
Scikit-learn
Pandas / NumPy
Flask
HTML / CSS / JavaScript
PyMuPDF
PyPDF
Tesseract OCR
PDF2Image

## 💻 Installation & Setup

### 1. Clone the repository

``bash
git clone https://github.com/yuguda30/mail-sentinel-ai.git
cd mail-sentinel-ai

### 2. Create virtual environment 

python -m venv .venv

Activate it:
Windows:
.venv\Scripts\activate 

### 3. Install dependencies

pip install -r requirements.txt

### 4. Setup OCR (IMPORTANT for PDF detection)

Install:

Tesseract OCR
Poppler

Then update paths in app.py:
   TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   POPPLER_PATH = r"C:\Users\HP\Downloads\poppler-25.12.0\Library\bin"

### 5. Run the Application
python app.py

Open browser:
http://127.0.0.1:5000


### How to Use
## Option 1: Paste Email
Paste email text
Click Analyze
View prediction result

## Option 2: Upload PDF
Upload email PDF
System extracts text (including OCR if needed)
Displays phishing analysis


### Output Explanation
Result: Phishing / Legitimate
Confidence: Model certainty (%)
Probability: Raw prediction value
Risk Level: Confidence strength
Summary: Interpretation of result

### Example Output
Legitimate Email:
  Result: Legitimate
  Confidence: 99.81%
  Risk Level: Low Risk

Phishing Email:
  Result: Phishing
  Confidence: 93.33%
  Risk Level: High Risk


### | Endpoint        | Method | Description          |
| --------------- | ------ | -------------------- |
| `/predict-text` | POST   | Analyze text input   |
| `/predict-pdf`  | POST   | Analyze uploaded PDF |


### Visualizations
The system generates:
   📊 Dataset Class Distribution
   📈 Accuracy Curve
   📉 Loss Curve
   🔲 Confusion Matrix


### Use Cases
Email security systems
Organizational cybersecurity tools
Fraud detection systems
User awareness tools


### Documentation
Full project documentation (Chapters 1–5):

👉 View Project Documentation


### Author
Muhammad Yuguda
BSc Cybersecurity
Alhikmah University Ilorin


### Future Improvements
Real-time email API integration
Real-time phishing detection Browser extension
Mobile application
Deployment on cloud (Azure/AWS /Render / Railway)
Advanced NLP (BERT, Transformers)
Improve UI with dashboard analytics
Expand dataset for higher generalization


### License
This project is for academic and research purposes.
