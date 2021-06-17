import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# this function group the countries into "Others" whose data is less tha cutoff count
def clean_countries(catg,cutoff):
    c_map = {}
    for i in range(len(catg)):
        if catg.values[i]>=cutoff:
            c_map[catg.index[i]]=catg.index[i]
        else:
            c_map[catg.index[i]] = 'Others'
    return c_map

# this function will convert the string values to float as per the conditions
def clean_xp(x):
    if x=='More than 50 years':
        return 50
    if x=='Less than 1 year':
        return 0.5
    return float(x)

# this function will clean the Education Level Data
def clean_Edu(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"

# store the cache for already executed data
@st.cache
def loadData():
    data = pd.read_csv("survey_results_public.csv")

    data = data[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]  # taking only 5 columns

    # cleaning the data (removing rows containing unusual data)
    data = data.rename({"ConvertedComp": "Salary"}, axis=1)  # axis 1 represents column and axis 0 represents row
    data = data.dropna()  # remove the row having atleast one NULL/NaN value
    data = data[data["Employment"] == "Employed full-time"]  # only keep the data where full time working is there
    data = data.drop("Employment", axis=1)  # delete the column of employment

    # clean the country data with cutoff = 400
    c_map = clean_countries(data.Country.value_counts(), 400)
    data['Country'] = data['Country'].map(c_map)

    # keep the data where the most data is present
    data = data[data['Salary'] <= 250000]
    data = data[data['Salary'] >= 10000]
    data = data[data['Country'] != 'Others']

    # clean the Years of Experience and Educational Level fields
    data['YearsCodePro'] = data['YearsCodePro'].apply(clean_xp)
    data['EdLevel'] = data['EdLevel'].apply(clean_Edu)
    return data

data = loadData()

def showExpPage():
    st.title("Explore through Statistics")
    st.write("""### Stack Overflow Developer Survey Statistics""")
    dataD = data["Country"].value_counts()
    f1,ax1 = plt.subplots()
    ax1.pie(dataD,labels=dataD.index,autopct="%1.1f%%",startangle=0)
    ax1.axis("equal")
    st.text(" \n")
    st.write("""#### Number of Data from different Countries""")
    st.pyplot(f1)
    st.text(" \n")
    st.text(" \n")
    st.write("#### Mean Salary - Countries")
    dataD = data.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(dataD)
    st.write("#### Mean Salary - Experience")
    dataD = data.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(dataD)
    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.text(" \n")
    st.markdown(""" :heart: Made by Aman Vashistha """)

