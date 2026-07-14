import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

from database import create_database, insert_data, fetch_data
from sensor import get_sensor_data
from predict import predict_temperature

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Smart Predictive Weather Monitoring",
    page_icon="🌦",
    layout="wide"
)

create_database()

st.title("🌦 Smart Predictive Weather Monitoring Dashboard")
st.markdown("---")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Dashboard")

refresh = st.sidebar.checkbox("Generate New Sensor Reading", value=True)

st.sidebar.markdown("---")
st.sidebar.info(
    """
This project simulates an IoT weather monitoring system.

Features:
- Live Sensor Data
- SQLite Database
- ML Prediction
- Alerts
- Charts
- CSV Export
"""
)

# -----------------------------
# GENERATE SENSOR DATA
# -----------------------------
if refresh:
    data = get_sensor_data()

    insert_data(
        data["temperature"],
        data["humidity"],
        data["pressure"]
    )

# -----------------------------
# LOAD DATABASE
# -----------------------------
df = fetch_data()

if len(df) == 0:
    st.warning("No sensor data available.")
    st.stop()

latest = df.iloc[0]

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🌡 Temperature",
        f"{latest['temperature']} °C"
    )

with col2:
    st.metric(
        "💧 Humidity",
        f"{latest['humidity']} %"
    )

with col3:
    st.metric(
        "🌍 Pressure",
        f"{latest['pressure']} hPa"
    )

st.markdown("---")

# -----------------------------
# ML PREDICTION
# -----------------------------
prediction = predict_temperature(df)

if prediction is not None:

    st.success(
        f"🤖 Predicted Next Temperature : {prediction} °C"
    )

else:

    st.info(
        "Collect at least 5 readings to enable prediction."
    )

# -----------------------------
# ALERTS
# -----------------------------
if latest["temperature"] > 35:
    st.error("🔥 High Temperature Alert!")

if latest["humidity"] < 35:
    st.warning("⚠ Low Humidity!")

if latest["pressure"] < 990:
    st.warning("⚠ Low Pressure!")

st.markdown("---")

# -----------------------------
# CHARTS
# -----------------------------
left, right = st.columns(2)

with left:

    st.subheader("Temperature Trend")

    fig, ax = plt.subplots(figsize=(8,4))

    ax.plot(
        df["temperature"][::-1],
        marker="o"
    )

    ax.set_ylabel("Temperature")

    st.pyplot(fig)

with right:

    st.subheader("Humidity Trend")

    fig, ax = plt.subplots(figsize=(8,4))

    ax.plot(
        df["humidity"][::-1],
        marker="o"
    )

    ax.set_ylabel("Humidity")

    st.pyplot(fig)

st.subheader("Pressure Trend")

fig, ax = plt.subplots(figsize=(12,4))

ax.plot(
    df["pressure"][::-1],
    marker="o"
)

ax.set_ylabel("Pressure")

st.pyplot(fig)

# -----------------------------
# DATABASE TABLE
# -----------------------------
st.markdown("---")

st.subheader("Sensor History")

st.dataframe(df)

# -----------------------------
# DOWNLOAD CSV
# -----------------------------
csv = df.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    file_name="weather_data.csv",
    mime="text/csv"
)

# -----------------------------
# LAST UPDATED
# -----------------------------
st.markdown("---")

st.caption(
    f"Last Updated : {latest['timestamp']}"
)