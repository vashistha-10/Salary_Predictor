import streamlit as st
import pickle
import numpy as np

def loadModel():
    with open("RModel.pkl", "rb") as file:
        dataS = pickle.load(file)
    return dataS

dataS = loadModel()
regressor_loaded = dataS["model"]
enc_country = dataS["enc_country"]
enc_edu = dataS["enc_edu"]

def show_predictPage():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need Information to predict the salary""")
    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden"
    )
    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad"
    )

    country = st.selectbox("Country",countries)
    education = st.selectbox("Education Level",education)
    exp = st.slider("Years of Experience",0,50,3)
    y = st.selectbox("Currency",["INR","US Dollars"])
    x = st.button("Predict Salary")
    if x:
        X = np.array([[country, education, exp]])
        X[:, 0] = enc_country.transform(X[:, 0])
        X[:, 1] = enc_edu.transform(X[:, 1])
        X = X.astype(float)
        salary = regressor_loaded.predict(X)
        if(y=="INR"):
            salary=salary*73.96
            st.subheader(f"Predicted Salary: INR {salary[0]:.2f}")
        else:
            st.subheader(f"Predicted Salary: $ {salary[0]:.2f}")

    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.markdown(""" :heart: Made by Aman Vashistha """)
