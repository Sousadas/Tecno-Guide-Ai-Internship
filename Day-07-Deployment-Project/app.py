import os
import joblib
import pandas as pd
import streamlit as st

# Define path to the model from Day-06
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'Day-06-Machine-Learning', 'model.pkl')

st.title('Simple House Price Predictor')

if os.path.exists(model_path):
    model = joblib.load(model_path)
    
    # Input field for area (sq m)
    area = st.number_input('Area (sq m)', min_value=10, max_value=1000, value=50, step=5)
    
    if st.button('Predict'):
        # Prepare input matching feature name 'area'
        input_data = pd.DataFrame([[area]], columns=['area'])
        prediction = model.predict(input_data)[0]
        st.success(f'Predicted Price: ${prediction:,.2f}')
else:
    st.error(f'Model file not found at {model_path}. Please run house_price_predictor.py first.')

