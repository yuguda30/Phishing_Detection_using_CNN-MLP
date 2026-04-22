import pandas as pd


def main():
    file_path = "../data/phishing_email.csv"
    df = pd.read_csv(file_path)

    print("First 5 rows:")
    print(df.head())

    print("\nDataset info:")
    print(df.info())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nLabel distribution:")
    print(df["label"].value_counts())

    print("\nShape:")
    print(df.shape)


if __name__ == "__main__":
    main()