from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TRAIN = DATA_DIR / "train.csv"
TEST = DATA_DIR / "test.csv"
PRED_OUT = DATA_DIR / "predictions.csv"

def log(msg: str):
    print(f"[INFO] {msg}")

def basic_fe(df: pd.DataFrame, is_train: bool) -> pd.DataFrame:
    """Minimal, reproducible FE with explicit prints (Q19)."""
    before_cols = list(df.columns)
    log(f"FE start | is_train={is_train} | cols={before_cols}")

    # Example: fill a few common Titanic fields if present
    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna(df["Age"].median())
        log("Filled Age NaNs with median")

    if "Fare" in df.columns:
        df["Fare"] = df["Fare"].fillna(df["Fare"].median())
        log("Filled Fare NaNs with median")

    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].fillna("S")
        log("Filled Embarked NaNs with 'S'")

    # Example: simple derived feature (family size)
    if {"SibSp", "Parch"}.issubset(df.columns):
        df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
        log("Created FamilySize = SibSp + Parch + 1")

    # Choose a small, consistent set of predictors if present
    candidate = ["Pclass", "Sex", "Age", "Fare", "Embarked", "FamilySize"]
    features = [c for c in candidate if c in df.columns]
    log(f"Selected base features: {features}")

    # One-hot encode categoricals (drop_first=True keeps it compact)
    df_enc = pd.get_dummies(df[features], drop_first=True)
    log(f"One-hot encoded -> shape={df_enc.shape} | cols={list(df_enc.columns)}")

    return df_enc

def main():
    # 1) Load train
    log(f"Loading TRAIN: {TRAIN}")
    train_df = pd.read_csv(TRAIN)
    log(f"TRAIN shape={train_df.shape}")
    log(f"TRAIN head:\n{train_df.head(3).to_string(index=False)}")

    # 2) Split X/y
    if "Survived" not in train_df.columns:
        raise ValueError("Column 'Survived' not found in train.csv")
    y = train_df["Survived"].astype(int)
    X = basic_fe(train_df, is_train=True)

    # Keep track of the columns we used so we can align test later
    fe_cols = X.columns.tolist()
    log(f"Train FE columns saved ({len(fe_cols)}): {fe_cols}")

    # 3) Scale numeric features (optional but prints help)
    scaler = StandardScaler(with_mean=False)  # sparse-friendly choice
    X_scaled = scaler.fit_transform(X)
    log(f"Scaled train features -> type={type(X_scaled)}, shape={X_scaled.shape}")

    # 4) Train/test split to report a training accuracy
    X_tr, X_va, y_tr, y_va = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    log(f"Split: X_tr={X_tr.shape}, X_va={X_va.shape}")

    # 5) Train model
    log("Training LogisticRegression...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_tr, y_tr)
    log("Training complete.")

    # 6) Accuracy on holdout from train
    va_pred = model.predict(X_va)
    acc = accuracy_score(y_va, va_pred)
    log(f"Training holdout accuracy: {acc:.4f}")

    # 7) Load test and apply SAME transforms
    log(f"Loading TEST: {TEST}")
    test_df = pd.read_csv(TEST)
    log(f"TEST shape={test_df.shape}")
    log(f"TEST head:\n{test_df.head(3).to_string(index=False)}")

    X_test = basic_fe(test_df, is_train=False)

    # Align columns exactly to train FE (add missing, order same)
    for col in fe_cols:
        if col not in X_test.columns:
            X_test[col] = 0
    X_test = X_test[fe_cols]
    log(f"Aligned test FE -> shape={X_test.shape}")

    X_test_scaled = scaler.transform(X_test)
    log(f"Scaled test features -> shape={X_test_scaled.shape}")

    # 8) Predict and save
    test_pred = model.predict(X_test_scaled)
    out = pd.DataFrame({"Survived_pred": test_pred})
    out.to_csv(PRED_OUT, index=False)
    log(f"Saved predictions to {PRED_OUT}")
    log(f"Predictions head:\n{out.head(5).to_string(index=False)}")

if __name__ == "__main__":
    main()
