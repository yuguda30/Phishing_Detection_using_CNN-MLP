import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

VOCAB_SIZE = 5000
MAX_LENGTH = 100


def main():
    file_path = "../data/phishing_email_cleaned.csv"

    df = pd.read_csv(file_path)

    # Fix missing/non-string text values
    df["clean_text"] = df["clean_text"].fillna("").astype(str)

    # Remove rows with empty cleaned text
    df = df[df["clean_text"].str.strip() != ""]

    # Make sure label is integer
    df["label"] = df["label"].astype(int)

    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
    tokenizer.fit_on_texts(df["clean_text"])

    sequences = tokenizer.texts_to_sequences(df["clean_text"])
    padded_sequences = pad_sequences(
        sequences,
        maxlen=MAX_LENGTH,
        padding="post",
        truncating="post"
    )

    X = padded_sequences
    y = np.array(df["label"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("y_train shape:", y_train.shape)
    print("y_test shape:", y_test.shape)

    # Save arrays
    np.save("../models/X_train.npy", X_train)
    np.save("../models/X_test.npy", X_test)
    np.save("../models/y_train.npy", y_train)
    np.save("../models/y_test.npy", y_test)

    # Save tokenizer
    with open("../models/tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)

    # Save config
    config = {
        "vocab_size": VOCAB_SIZE,
        "max_length": MAX_LENGTH,
        "embedding_dim": 64
    }

    with open("../models/model_config.json", "w") as f:
        json.dump(config, f)

    print("\nTokenized data, split arrays, tokenizer, and config saved successfully.")


if __name__ == "__main__":
    main()