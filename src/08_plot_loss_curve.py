import json
import matplotlib.pyplot as plt

def main():
    with open("../outputs/training_history.json", "r") as f:
        history = json.load(f)

    plt.figure(figsize=(8, 5))
    plt.plot(history["loss"], label="Training Loss", color="blue")
    plt.plot(history["val_loss"], label="Validation Loss", color="orange")
    plt.title("Training and Validation Loss over Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("../outputs/loss_curve.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()