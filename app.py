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
# Day type input
# -----------------------------

day_type = st.selectbox(
    "Day Type",
    ["Weekday", "Weekend"]
)

is_weekend = 1 if day_type == "Weekend" else 0


# -----------------------------
# Time input
# -----------------------------

time_options = []

for hour in range(24):

    if hour == 0:
        label = "12 AM"

    elif hour < 12:
        label = f"{hour} AM"

    elif hour == 12:
        label = "12 PM"

    else:
        label = f"{hour - 12} PM"

    time_options.append(label)


selected_time = st.select_slider(
    "Time of Day",
    options=time_options,
    value="5 PM"
)


# Convert display time back to 0-23 hour

hour = time_options.index(selected_time)


# -----------------------------
# Prediction
# -----------------------------

input_data = pd.DataFrame({
    "hour": [hour],
    "is_weekend": [is_weekend]
})

predicted_speed = model.predict(
    input_data
)[0]


# -----------------------------
# Traffic condition
# -----------------------------

if predicted_speed >= 60:
    condition = "🟢 Free Flow"

elif predicted_speed >= 50:
    condition = "🟡 Moderate Traffic"

elif predicted_speed >= 40:
    condition = "🟠 Congested"

else:
    condition = "🔴 Heavy Congestion"


# -----------------------------
# Display result automatically
# -----------------------------

st.divider()

st.subheader("Predicted Traffic Speed")

st.metric(
    label=f"{day_type} at {selected_time}",
    value=f"{predicted_speed:.1f} mph"
)

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