import streamlit as st
st.title('Simple Deployment Demo')
area = st.number_input('Area (sq m)', min_value=10)
if st.button('Predict'):
    st.write('This is where prediction would appear')
