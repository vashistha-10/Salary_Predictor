import streamlit as st
from predict import show_predictPage
from explore import showExpPage

option = st.sidebar.selectbox("Explore or Predict",("Predict","Explore"))
if(option=="Predict"):
    show_predictPage()
else:
    showExpPage()