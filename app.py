import streamlit as st
import pandas as pd
import joblib
import os

st.title("📱 5G Phone Price Prediction System")

# ---- FILE CHECK ----
if not os.path.exists("price_model.pkl"):
    st.error("❌ price_model.pkl file not found")
    st.stop()

if not os.path.exists("phones_5g.csv"):
    st.error("❌ phones_5g.csv file not found")
    st.stop()

# ---- LOAD FILES ----
model = joblib.load("price_model.pkl")
data = pd.read_csv("phones_5g.csv")

st.success("✅ Model & Dataset Loaded Successfully")

st.write("Price Range: ₹20,000 – ₹30,000")

ram = st.selectbox("RAM (GB)", [6, 8, 12])
storage = st.selectbox("Storage (GB)", [128, 256])
battery = st.slider("Battery (mAh)", 4000, 6000, 5000)
camera = st.selectbox("Camera (MP)", [48, 50, 64])
processor = st.slider("Processor Score", 700, 850, 750)

if st.button("Predict Price"):
    price = model.predict([[ram, storage, battery, camera, processor]])
    st.success(f"Predicted Price: ₹{int(price[0])}")

    st.subheader("🔝 Top 3 Recommended 5G Phones")
    rec = data.sort_values(by="Price").head(3)
    st.table(rec[['Brand','RAM','Storage','Camera','Price']])
