from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TRAIN = DATA_DIR / "train.csv"

def main():
    print(f"[INFO] Loading: {TRAIN}")
    df = pd.read_csv(TRAIN)
    print("[OK] Loaded train.csv")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head().to_string(index=False))

if __name__ == "__main__":
    main()
