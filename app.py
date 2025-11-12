import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load('wpt_efficiency_model.pkl')
columns = [
    'turns', 'gap', 'offset', 'frequency', 'q_factor', 'voltage', 'current',
    'coil_geometry_circle', 'coil_geometry_d-shaped', 'coil_geometry_pancake',
    'ferrite_A1', 'ferrite_B1', 'shield_none', 'shield_mu-metal'
]

st.title("WPT Efficiency ML Predictor")

coil_geometry = st.selectbox("Coil Geometry", ["circle", "d-shaped", "pancake"])
turns = st.number_input("Turns", min_value=1, max_value=50, value=10)
gap = st.slider("Gap (mm)", 5, 30, 15)
offset = st.slider("Offset (mm)", 0, 20, 0)
frequency = st.selectbox("Frequency (kHz)", [80, 90, 100])
q_factor = st.selectbox("Q Factor", [150, 170, 200])
voltage = st.selectbox("Voltage (V)", [300, 350, 400])
current = st.selectbox("Current (A)", [3, 5, 7])
ferrite = st.selectbox("Ferrite", ["A1", "B1"])
shield = st.selectbox("Shield", ["none", "mu-metal"])

sample = dict.fromkeys(columns, 0)
sample['turns'] = turns
sample['gap'] = gap
sample['offset'] = offset
sample['frequency'] = frequency
sample['q_factor'] = q_factor
sample['voltage'] = voltage
sample['current'] = current
sample[f'coil_geometry_{coil_geometry}'] = 1
sample[f'ferrite_{ferrite}'] = 1
sample[f'shield_{shield}'] = 1

sample_df = pd.DataFrame([sample])[columns]

if st.button("Predict Efficiency"):
    prediction = model.predict(sample_df)
    st.success(f"Predicted Efficiency: {prediction[0]:.2f}%")
