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
# ================= FIX START =================

# Clean all column names
data.columns = data.columns.str.strip().str.lower()

# Automatically find price column
price_col = None
for col in data.columns:
    if 'price' in col or 'cost' in col or 'amount' in col:
        price_col = col
        break

if price_col is None:
    st.error("❌ Price column not found in dataset")
    st.stop()

# Rename found column to standard name
data.rename(columns={price_col: 'Price'}, inplace=True)

# ================= FIX END =================

# 🔧 CLEAN COLUMN NAMES COMPLETELY
data.columns = (
    data.columns
    .str.strip()        # remove spaces
    .str.lower()        # convert to lowercase
)

# 🔧 FORCE PRICE COLUMN NAME
if 'price' in data.columns:
    data.rename(columns={'price': 'Price'}, inplace=True)

# 🔹 COLUMN CLEANING (VERY IMPORTANT)
data.columns = data.columns.str.strip()

# 🔹 PRICE COLUMN FIX
if 'price' in data.columns:
    data.rename(columns={'price': 'Price'}, inplace=True)


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

    rec = data.sort_values(by='Price', ascending=True).head(3)

    st.table(rec[['Brand', 'RAM', 'Storage', 'Camera', 'Price']])





