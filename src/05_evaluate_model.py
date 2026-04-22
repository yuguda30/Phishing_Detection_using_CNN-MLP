import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from tensorflow.keras.models import load_model


def main():
    X_test = np.load("../models/X_test.npy")
    y_test = np.load("../models/y_test.npy")

    model = load_model("../models/best_phishing_cnn_mlp.keras")

    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype("int32").flatten()

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)

    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    report = classification_report(y_test, y_pred)
    print("\nClassification Report:")
    print(report)

    # Save report
    with open("../outputs/classification_report.txt", "w") as f:
        f.write(report)

    # Plot confusion matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Legitimate", "Phishing"],
        yticklabels=["Legitimate", "Phishing"]
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.savefig("../outputs/confusion_matrix.png")
    plt.show()

    print("\nEvaluation complete. Outputs saved in outputs/ folder.")


if __name__ == "__main__":
    main()