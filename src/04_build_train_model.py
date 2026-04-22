import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential


def main():
    # Load data
    X_train = np.load("../models/X_train.npy")
    X_test = np.load("../models/X_test.npy")
    y_train = np.load("../models/y_train.npy")
    y_test = np.load("../models/y_test.npy")

    # Load config
    with open("../models/model_config.json", "r") as f:
        config = json.load(f)

    vocab_size = config["vocab_size"]
    max_length = config["max_length"]
    embedding_dim = config["embedding_dim"]

    # Build model
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
        Conv1D(filters=128, kernel_size=5, activation="relu"),
        MaxPooling1D(pool_size=2),
        Flatten(),
        Dense(64, activation="relu"),
        Dropout(0.5),
        Dense(1, activation="sigmoid")
    ])

    model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )

    model.summary()

    # Callbacks
    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=2,
        restore_best_weights=True
    )

    checkpoint = ModelCheckpoint(
        "../models/best_phishing_cnn_mlp.keras",
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    )

    # Train model
    history = model.fit(
        X_train,
        y_train,
        epochs=5,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping, checkpoint]
    )

    # Save final model
    model.save("../models/final_phishing_cnn_mlp.keras")

    # Save training history for later plotting
    with open("../outputs/training_history.json", "w") as f:
        json.dump(history.history, f)

    # Accuracy plot
    plt.figure(figsize=(8, 5))
    plt.plot(history.history["accuracy"], label="Training Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("../outputs/accuracy_plot.png", dpi=300)
    plt.show()

    # Loss plot
    plt.figure(figsize=(8, 5))
    plt.plot(history.history["loss"], label="Training Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("../outputs/loss_plot.png", dpi=300)
    plt.show()

    print("\nTraining complete. Model, plots, and training history saved.")


if __name__ == "__main__":
    main()