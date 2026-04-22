import json
import pickle
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text: str) -> str:
    stop_words = set(stopwords.words("english"))
    return " ".join([word for word in text.split() if word not in stop_words])


def load_resources():
    model = load_model("../models/best_phishing_cnn_mlp.keras")

    with open("../models/tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)

    with open("../models/model_config.json", "r") as f:
        config = json.load(f)

    return model, tokenizer, config


def predict_email(email_text: str):
    model, tokenizer, config = load_resources()
    max_length = config["max_length"]

    cleaned = clean_text(email_text)
    cleaned = remove_stopwords(cleaned)

    seq = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(seq, maxlen=max_length, padding="post", truncating="post")

    prob = model.predict(padded, verbose=0)[0][0]
    pred = 1 if prob > 0.5 else 0

    print("\nOriginal Email:\n")
    print(email_text)
    print("\nCleaned Email:\n")
    print(cleaned)
    print("\nPrediction Probability:", round(float(prob), 4))

    if pred == 1:
        print("Prediction: Phishing Email")
    else:
        print("Prediction: Legitimate Email")


def main():
    email_input = input("Dear user, your account has been temporarily suspended. Click the link below immediately to verify your identity and restore access: http://secure-verification-login.com\:")
    predict_email(email_input)


if __name__ == "__main__":
    main()