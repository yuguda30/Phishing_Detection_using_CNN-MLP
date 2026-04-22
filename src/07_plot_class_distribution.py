import pandas as pd
import matplotlib.pyplot as plt

def main():
    file_path = "../data/phishing_email_cleaned.csv"
    df = pd.read_csv(file_path)

    class_counts = df["label"].value_counts().sort_index()
    labels = ["Legitimate", "Phishing"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, class_counts, color=["#4CAF50", "#E53935"])
    plt.title("Dataset Class Distribution")
    plt.xlabel("Class")
    plt.ylabel("Number of Samples")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 200,
                 f"{int(height)}", ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig("../outputs/class_distribution.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()