"""
GSRTC Bus Arrival Time & Delay Prediction - single file project
Dataset repository: https://github.com/basic30/ETA-Prediction-Dataset
Dataset is synthetic, not official GSRTC operational data.

Place this file alongside bus_gps_data.csv, historical_data.csv, route_data.csv.
Install: pip install pandas numpy matplotlib seaborn scikit-learn joblib
Run: python gsrtc_bus_prediction.py
"""
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, classification_report,
    ConfusionMatrixDisplay)

ROOT = Path(__file__).resolve().parent
GPS_PATH = ROOT / "bus_gps_data.csv"
HIST_PATH = ROOT / "historical_data.csv"
ROUTE_PATH = ROOT / "route_data.csv"
OUT = ROOT / "gsrtc_outputs"
PLOTS = OUT / "plots"
MODELS = OUT / "models"
SEED, TEST_SIZE = 42, 0.20
CLASS_LABELS = ["On-time", "Minor Delay", "Major Delay"]

def section(title):
    print("\\n" + "=" * 70 + "\\n" + title + "\\n" + "=" * 70)

def read_optional(path, name):
    if not path.exists():
        print(f"[Warning] {name} not found: {path.name}")
        return None
    data = pd.read_csv(path)
    print(f"{name}: {data.shape} | columns={list(data.columns)}")
    print(data.head(3), "\\n")
    return data

def save_plot(filename):
    plt.tight_layout()
    plt.savefig(PLOTS / filename, dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()

def preprocessor(features):
    cat = ["route_id"]
    nums = ["time_slot", "avg_speed"]
    return ColumnTransformer([
        ("route", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), cat),
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scale", StandardScaler())
        ]), nums)
    ])

def main():
    OUT.mkdir(exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)

    section("1. LOAD CSV FILES")
    gps = read_optional(GPS_PATH, "GPS data")
    hist = read_optional(HIST_PATH, "Historical data")
    routes = read_optional(ROUTE_PATH, "Route data")
    if hist is None:
        raise FileNotFoundError("historical_data.csv is missing. Place it beside this script.")

    section("2. DATA INSPECTION")
    print("Historical shape:", hist.shape)
    print("\\nMissing values:\\n", hist.isnull().sum())
    print("Duplicate rows:", hist.duplicated().sum())
    print("\\nSummary:\\n", hist.describe(include="all"))

    section("3. DATA CLEANING")
    df = hist.copy()
    df.columns = df.columns.str.strip()
    needed = ["route_id", "time_slot", "avg_speed", "avg_delay_minutes"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Expected columns missing: {missing}; actual columns: {list(df.columns)}")
    df = df.drop_duplicates()
    df["route_id"] = df["route_id"].astype("string").str.strip()
    for col in ["time_slot", "avg_speed", "avg_delay_minutes"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[~df["time_slot"].between(0, 23), "time_slot"] = np.nan
    df.loc[df["avg_speed"] <= 0, "avg_speed"] = np.nan
    # For this beginner project, negative delays (early arrivals) are treated as invalid.
    df.loc[df["avg_delay_minutes"] < 0, "avg_delay_minutes"] = np.nan
    df = df.dropna(subset=needed).reset_index(drop=True)
    df["time_slot"] = df["time_slot"].astype(int)
    if len(df) < 10:
        raise ValueError(f"Only {len(df)} usable rows after cleaning; need at least 10.")
    df.to_csv(OUT / "cleaned_historical_data.csv", index=False)
    print("Cleaned dataset shape:", df.shape)
    print("Saved cleaned CSV to:", OUT / "cleaned_historical_data.csv")

    section("4. EDA")
    print("Mean delay by route:\\n", df.groupby("route_id")["avg_delay_minutes"].mean().sort_values(ascending=False))
    print("Mean delay by hour:\\n", df.groupby("time_slot")["avg_delay_minutes"].mean().sort_index())

    plt.figure(figsize=(8, 5))
    sns.histplot(df["avg_delay_minutes"], bins=20, kde=True)
    plt.title("Delay Distribution"); plt.xlabel("Delay (minutes)")
    save_plot("01_delay_distribution.png")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="avg_speed", y="avg_delay_minutes", hue="route_id")
    plt.title("Average Speed vs Delay")
    save_plot("02_speed_vs_delay.png")

    plt.figure(figsize=(9, 5))
    sns.barplot(data=df.groupby("time_slot", as_index=False)["avg_delay_minutes"].mean(),
                x="time_slot", y="avg_delay_minutes")
    plt.title("Average Delay by Hour"); plt.xlabel("Hour (0-23)")
    save_plot("03_delay_by_hour.png")

    plt.figure(figsize=(9, 5))
    sns.barplot(data=df.groupby("route_id", as_index=False)["avg_delay_minutes"].mean(),
                x="route_id", y="avg_delay_minutes")
    plt.title("Average Delay by Route"); plt.xticks(rotation=45)
    save_plot("04_delay_by_route.png")

    plt.figure(figsize=(7, 5))
    sns.heatmap(df[["time_slot", "avg_speed", "avg_delay_minutes"]].corr(),
                annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    save_plot("05_correlation.png")

    features = ["route_id", "time_slot", "avg_speed"]

    section("5. REGRESSION: PREDICT DELAY MINUTES")
    Xr, yr = df[features], df["avg_delay_minutes"]
    X_train, X_test, y_train, y_test = train_test_split(
        Xr, yr, test_size=TEST_SIZE, random_state=SEED)
    regressors = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=150, random_state=SEED)
    }
    reg_rows, best_reg, best_reg_mae, best_reg_name = [], None, float("inf"), None
    for name, model in regressors.items():
        pipe = Pipeline([("prep", preprocessor(features)), ("model", model)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))
        r2 = r2_score(y_test, pred)
        reg_rows.append({"Model": name, "MAE_minutes": mae, "RMSE_minutes": rmse, "R2": r2})
        print(f"{name}: MAE={mae:.3f} min | RMSE={rmse:.3f} | R2={r2:.3f}")
        if mae < best_reg_mae:
            best_reg, best_reg_mae, best_reg_name = pipe, mae, name
    reg_results = pd.DataFrame(reg_rows).sort_values("MAE_minutes")
    reg_results.to_csv(OUT / "regression_model_comparison.csv", index=False)
    print("\\nRegression comparison:\\n", reg_results)

    reg_pred = best_reg.predict(X_test)
    plt.figure(figsize=(7, 5))
    sns.scatterplot(x=y_test, y=reg_pred)
    plt.xlabel("Actual delay"); plt.ylabel("Predicted delay")
    plt.title(f"Actual vs Predicted - {best_reg_name}")
    save_plot("06_regression_actual_predicted.png")

    section("6. CLASSIFICATION: DELAY CATEGORY")
    # Class thresholds are chosen for this student project, not official GSRTC rules.
    df["delay_status"] = pd.cut(df["avg_delay_minutes"],
        bins=[-np.inf, 10, 30, np.inf],
        labels=CLASS_LABELS, right=True, include_lowest=True)
    print("Class frequencies:\\n", df["delay_status"].value_counts())
    Xc, yc = df[features], df["delay_status"].astype(str)
    counts = yc.value_counts()
    stratify = yc if (len(counts) > 1 and counts.min() >= 2) else None
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        Xc, yc, test_size=TEST_SIZE, random_state=SEED, stratify=stratify)
    classifiers = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Random Forest Classifier": RandomForestClassifier(
            n_estimators=150, random_state=SEED, class_weight="balanced")
    }
    cls_rows, best_cls, best_f1, best_cls_name = [], None, -1, None
    for name, model in classifiers.items():
        pipe = Pipeline([("prep", preprocessor(features)), ("model", model)])
        pipe.fit(Xc_train, yc_train)
        pred = pipe.predict(Xc_test)
        acc = accuracy_score(yc_test, pred)
        prec = precision_score(yc_test, pred, average="weighted", zero_division=0)
        rec = recall_score(yc_test, pred, average="weighted", zero_division=0)
        f1 = f1_score(yc_test, pred, average="weighted", zero_division=0)
        cls_rows.append({"Model": name, "Accuracy": acc, "Weighted_Precision": prec,
                         "Weighted_Recall": rec, "Weighted_F1": f1})
        print(f"\\n{name}: Accuracy={acc:.3f} | Precision={prec:.3f} | Recall={rec:.3f} | F1={f1:.3f}")
        print(classification_report(yc_test, pred, zero_division=0))
        ConfusionMatrixDisplay.from_predictions(yc_test, pred)
        plt.title(f"Confusion Matrix - {name}")
        save_plot("07_confusion_" + name.lower().replace(" ", "_") + ".png")
        if f1 > best_f1:
            best_cls, best_f1, best_cls_name = pipe, f1, name
    cls_results = pd.DataFrame(cls_rows).sort_values("Weighted_F1", ascending=False)
    cls_results.to_csv(OUT / "classification_model_comparison.csv", index=False)
    print("\\nClassification comparison:\\n", cls_results)

    section("7. SAVE MODELS")
    import joblib
    joblib.dump(best_reg, MODELS / "best_regression_model.joblib")
    joblib.dump(best_cls, MODELS / "best_classification_model.joblib")
    print("Saved best regression:", best_reg_name)
    print("Saved best classification:", best_cls_name)
    print("Model files saved under:", MODELS)

    section("8. SAMPLE PREDICTION")
    sample = pd.DataFrame([{
        "route_id": str(df["route_id"].iloc[0]),
        "time_slot": int(df["time_slot"].median()),
        "avg_speed": float(df["avg_speed"].median())
    }])
    delay_pred = best_reg.predict(sample)[0]
    status_pred = best_cls.predict(sample)[0]
    print("Input sample:", sample.to_dict(orient="records")[0])
    print(f"Predicted delay: {delay_pred:.2f} minutes")
    print(f"Predicted class: {status_pred}")
    print("This is an example prediction from synthetic data, not live GSRTC information.")

    section("9. COMPLETED - OUTPUTS")
    print("Output folder:", OUT)
    print("Includes cleaned CSV, metric comparison CSVs, plots, and saved models.")
    print("Reminder: dataset is synthetic. Model performance on actual GSRTC data is unknown.")

if __name__ == "__main__":
    main()
