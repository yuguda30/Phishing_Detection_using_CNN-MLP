import re
import pandas as pd
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


def main():
    file_path = "../data/phishing_email.csv"
    output_path = "../data/phishing_email_cleaned.csv"

    df = pd.read_csv(file_path)

    df = df.dropna()
    df = df.drop_duplicates()

    df["clean_text"] = df["text_combined"].apply(clean_text)
    df["clean_text"] = df["clean_text"].apply(remove_stopwords)

    print("Preview of cleaned data:")
    print(df[["text_combined", "clean_text", "label"]].head())

    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved to: {output_path}")


if __name__ == "__main__":
    main()