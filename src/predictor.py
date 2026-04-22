import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.utils import preprocess_text

MODEL_PATH = "models/best_phishing_cnn_mlp.keras"
TOKENIZER_PATH = "models/tokenizer.pkl"
CONFIG_PATH = "models/model_config.json"

_model = None
_tokenizer = None
_config = None


def load_resources():
    global _model, _tokenizer, _config

    if _model is None:
        _model = load_model(MODEL_PATH)

    if _tokenizer is None:
        with open(TOKENIZER_PATH, "rb") as f:
            _tokenizer = pickle.load(f)

    if _config is None:
        with open(CONFIG_PATH, "r") as f:
            _config = json.load(f)

    return _model, _tokenizer, _config


def predict_email_text(email_text: str):
    model, tokenizer, config = load_resources()
    max_length = config["max_length"]

    processed = preprocess_text(email_text)

    seq = tokenizer.texts_to_sequences([processed])
    padded = pad_sequences(seq, maxlen=max_length, padding="post", truncating="post")

    prob = float(model.predict(padded, verbose=0)[0][0])
    label = "Phishing" if prob > 0.5 else "Legitimate"
    confidence = prob * 100 if prob > 0.5 else (1 - prob) * 100

    # Confidence level = how sure the model is
    if confidence >= 90:
        confidence_level = "High"
    elif confidence >= 75:
        confidence_level = "Moderate"
    else:
        confidence_level = "Low"

    # Risk status = danger level of the email itself
    if label == "Phishing":
        risk_status = "High Risk"
        summary = "The model detected phishing-like language patterns and classified this message as suspicious."
    else:
        risk_status = "Low Risk"
        summary = "The model found the message more consistent with legitimate email patterns."

    return {
        "label": label,
        "probability": round(prob, 4),
        "confidence": round(confidence, 2),
        "confidence_level": confidence_level,
        "risk_status": risk_status,
        "summary": summary,
        "processed_text": processed
    }