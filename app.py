import streamlit as st
import pandas as pd
import joblib
import os

# ------------------ TITLE ------------------
st.title("📱 5G Phone Price Prediction System")

# ------------------ FILE CHECK ------------------
if not os.path.exists("price_model.pkl"):
    st.error("❌ price_model.pkl file not found")
    st.stop()

if not os.path.exists("phones_5g.csv"):
    st.error("❌ phones_5g.csv file not found")
    st.stop()

# ------------------ LOAD FILES ------------------
model = joblib.load("price_model.pkl")
data = pd.read_csv("phones_5g.csv")

# ------------------ COLUMN CLEANING (ROOT FIX) ------------------
data.columns = data.columns.str.strip().str.lower()

# find price column automatically
price_col = None
for col in data.columns:
    if "price" in col:
        price_col = col
        break

if price_col is None:
    st.error("❌ Price column not found in dataset")
    st.stop()

# rename to standard name
data.rename(columns={price_col: "price"}, inplace=True)

st.success("✅ Model & Dataset Loaded Successfully")
st.write("Price Range: ₹20,000 – ₹30,000")

# ------------------ INPUTS ------------------
ram = st.selectbox("RAM (GB)", [6, 8, 12])
storage = st.selectbox("Storage (GB)", [128, 256])
battery = st.slider("Battery (mAh)", 4000, 6000, 5000)
camera = st.selectbox("Camera (MP)", [48, 50, 64])
processor = st.slider("Processor Score", 700, 850, 750)

# ------------------ PREDICTION ------------------
if st.button("Predict Price"):
    predicted_price = model.predict(
        [[ram, storage, battery, camera, processor]]
    )

    st.success(f"Predicted Price: ₹{int(predicted_price[0])}")

    # ------------------ TOP 3 RECOMMENDATION ------------------
    st.subheader("🔝 Top 3 Recommended 5G Phones")

    recommended = (
        data[
            (data["price"] >= 20000) &
            (data["price"] <= 30000)
        ]
        .sort_values(by="price")
        .head(3)
    )

    st.table(
        recommended[
            ["brand", "ram", "storage", "camera", "price"]
        ]
    )
