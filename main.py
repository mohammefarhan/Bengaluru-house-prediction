# =====================================
# 1. IMPORT LIBRARIES
# =====================================
import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor

# =====================================
# 2. LOAD DATA
# =====================================
df = pd.read_csv("Bengaluru_House_Data.csv")

print("Original Shape:", df.shape)

# =====================================
# 3. BASIC CLEANING
# =====================================
df = df.drop_duplicates()
df = df.dropna(subset=["price"])

# Extract BHK from size
df["bhk"] = df["size"].str.extract("(\d+)").astype(float)

# Convert total_sqft
def convert_sqft(x):
    try:
        if isinstance(x, str) and "-" in x:
            a, b = x.split("-")
            return (float(a) + float(b)) / 2
        return float(x)
    except:
        return np.nan

df["total_sqft"] = df["total_sqft"].apply(convert_sqft)

# Drop missing core values
df = df.dropna(subset=["total_sqft", "bath", "bhk"])

# =====================================
# 4. REMOVE OUTLIERS
# =====================================
df = df[df["total_sqft"] / df["bhk"] >= 300]

# =====================================
# 5. LOCATION CLEANING
# =====================================
df["location"] = df["location"].fillna("other")
loc_counts = df["location"].value_counts()

df["location"] = df["location"].apply(
    lambda x: x if loc_counts[x] >= 10 else "other"
)

# =====================================
# 6. SELECT FEATURES
# =====================================
y = df["price"]

X = df.drop(
    ["price", "size", "society", "availability"],
    axis=1,
    errors="ignore"
)

# 🚨 REMOVE DATA LEAKAGE FEATURE
if "price_per_sqft" in X.columns:
    X = X.drop("price_per_sqft", axis=1)

# One-hot encode categorical columns
X = pd.get_dummies(X, drop_first=True)

# Safety numeric conversion
X["total_sqft"] = pd.to_numeric(X["total_sqft"], errors="coerce")

X = X.dropna()
y = y.loc[X.index]

print("Final Training Shape:", X.shape)

# =====================================
# 7. TRAIN TEST SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================
# 8. GRID SEARCH (BEST MODEL)
# =====================================
gb = GradientBoostingRegressor(random_state=42)

param_grid = {
    "n_estimators": [100, 200],
    "learning_rate": [0.05, 0.1],
    "max_depth": [3, 4]
}

grid = GridSearchCV(
    gb,
    param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest Params:", grid.best_params_)

# =====================================
# 9. EVALUATION
# =====================================
train_pred = best_model.predict(X_train)
test_pred = best_model.predict(X_test)

print("\nTrain R2:", r2_score(y_train, train_pred))
print("Test R2 :", r2_score(y_test, test_pred))
print("MAE     :", mean_absolute_error(y_test, test_pred))

# =====================================
# 10. SAVE MODEL + FEATURE COLUMNS
# =====================================
with open("model_data.pkl", "wb") as f:
    pickle.dump({
        "model": best_model,
        "columns": X.columns
    }, f)

print("\nmodel_data.pkl saved successfully")
