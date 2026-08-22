import streamlit as st
import pandas as pd
import joblib


# -----------------------------
# Load trained model
# -----------------------------

model = joblib.load(
    "models/traffic_speed_model.pkl"
)


# -----------------------------
# Page
# -----------------------------

st.title("🚗 I-280 Traffic Speed Predictor")

st.write(
    "Estimate typical I-280 North traffic speed "
    "based on time of day and whether it is a "
    "weekday or weekend."
)

st.caption(
    "Model trained using historical Caltrans PeMS "
    "traffic sensor data."
)


# -----------------------------
# User input
# -----------------------------

day_type = st.selectbox(
    "Day Type",
    ["Weekday", "Weekend"]
)

hour = st.slider(
    "Hour of Day",
    min_value=0,
    max_value=23,
    value=17
)

display_hour = pd.Timestamp(
    year=2026,
    month=1,
    day=1,
    hour=hour
).strftime("%I %p")

st.caption(f"Selected time: {display_hour}")


# Convert user selection into model input

is_weekend = (
    1 if day_type == "Weekend" else 0
)


# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Speed"):

    input_data = pd.DataFrame({
        "hour": [hour],
        "is_weekend": [is_weekend]
    })

    predicted_speed = model.predict(
        input_data
    )[0]


    # -------------------------
    # Display result
    # -------------------------

    st.subheader(
        "Predicted Traffic Speed"
    )

    st.metric(
        label="Estimated Speed",
        value=f"{predicted_speed:.1f} mph"
    )


    # -------------------------
    # Traffic condition
    # -------------------------

    if predicted_speed >= 60:
        condition = "🟢 Free Flow"

    elif predicted_speed >= 50:
        condition = "🟡 Moderate Traffic"

    elif predicted_speed >= 40:
        condition = "🟠 Congested"

    else:
        condition = "🔴 Heavy Congestion"


    st.write(
        f"Traffic condition: **{condition}**"
    )


# -----------------------------
# Information
# -----------------------------

st.divider()

st.subheader("About This Project")

st.write(
    "This application uses a Random Forest "
    "regression model trained on 5-minute "
    "traffic observations from I-280 North "
    "monitoring stations in Santa Clara County."
)

st.write(
    "The current model uses two features: "
    "**hour of day** and **weekday/weekend status**."
)

st.info(
    "This is an educational traffic-pattern "
    "prediction model based on historical data, "
    "not a real-time traffic forecasting service."
)