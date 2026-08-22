import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/traffic_speed_model.pkl")

st.title("🚗 I-280 Traffic Speed Predictor")

st.write(
    "Estimate I-280 northbound traffic speed using "
    "a machine learning model trained on Caltrans PeMS data."
)

# User inputs
hour = st.slider(
    "Hour of Day",
    min_value=0,
    max_value=23,
    value=17
)

flow = st.slider(
    "Traffic Flow (vehicles / 5 min)",
    min_value=0,
    max_value=200,
    value=80
)

# Prediction
if st.button("Predict Speed"):

    input_data = pd.DataFrame({
        "hour": [hour],
        "flow": [flow]
    })

    predicted_speed = model.predict(input_data)[0]

    st.subheader("Predicted Traffic Speed")

    st.metric(
        label="Estimated Speed",
        value=f"{predicted_speed:.1f} mph"
    )