# 🏠 Bengaluru House Price Predictor

A premium machine learning web application that predicts property prices in Bengaluru using advanced regression models and a modern Streamlit dashboard.

Built using **Python, Machine Learning, Gradient Boosting, and Streamlit** with a clean and interactive UI.

---

## 🚀 Overview

This project estimates house prices based on multiple property features such as area, number of rooms, and location.

The application:

- Takes user property inputs
- Processes data using a trained ML model
- Predicts price instantly
- Displays results with an animated premium interface

---

## 🧠 How It Works

### 1. Data Preprocessing

- Handling missing values
- Extracting BHK from size column
- Cleaning and converting `total_sqft`
- Grouping rare locations
- One-hot encoding categorical features

---

### 2. Model Building

- Gradient Boosting Regressor
- GridSearchCV hyperparameter tuning
- Train/Test split validation
- Cross-validation evaluation

---

### 3. Deployment

- Streamlit web application
- Dynamic dropdown menus
- Premium dark UI
- Animated price prediction card

---
## 📂 Project Structure
│
├── app.py
├── train_model.py
├── model_data.pkl
├── requirements.txt
└── Bengaluru_House_Data.csv

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/house-price-predictor.git
cd house-price-predictor

## Install dependencies:
pip install -r requirements.txt

## Train the Model
python train_model.py

This will generate:
model_data.pkl

Run the App
streamlit run app.py


