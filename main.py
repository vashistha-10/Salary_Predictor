import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
import pickle

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

data = pd.read_csv("survey_results_public.csv")

data = data[["Country","EdLevel","YearsCodePro","Employment","ConvertedComp"]] # taking only 5 columns

# cleaning the data (removing rows containing unusual data)
data = data.rename({"ConvertedComp":"Salary"},axis=1) # axis 1 represents column and axis 0 represents row
data = data.dropna() # remove the row having atleast one NULL/NaN value
data = data[data["Employment"]=="Employed full-time"] # only keep the data where full time working is there
data = data.drop("Employment",axis=1) # delete the column of employment

# clean the country data with cutoff = 400
c_map = clean_countries(data.Country.value_counts(),400)
data['Country']=data['Country'].map(c_map)

# keep the data where the most data is present
data = data[data['Salary']<=250000]
data = data[data['Salary']>=10000]
data=data[data['Country']!='Others']

# clean the Years of Experience and Educational Level fields
data['YearsCodePro']=data['YearsCodePro'].apply(clean_xp)
data['EdLevel']=data['EdLevel'].apply(clean_Edu)

# encoding the educational level into numbers
enc_edu = LabelEncoder()
data['EdLevel'] = enc_edu.fit_transform(data['EdLevel']);

# encoding the country names into numbers
enc_country = LabelEncoder()
data['Country'] = enc_country.fit_transform(data['Country']);

# building the regression model by choosing best model using GridSearchCV
X = data.drop('Salary',axis=1)
y = data['Salary']
max_depth = [None,2,4,6,8,10,12]
params = {"max_depth":max_depth}
regressor = DecisionTreeRegressor(random_state=0)
gs = GridSearchCV(regressor,params,scoring="neg_mean_squared_error")
gs.fit(X, y.values)
regressor = gs.best_estimator_
regressor.fit(X,y.values)

# predicting the sample data
X = np.array([["United States", "Master’s degree", 15]])
X[:,0] = enc_country.transform(X[:,0])
X[:,1] = enc_edu.transform(X[:,1])
X = X.astype(float)
yP = regressor.predict(X)
print(yP)

# loading the regression model into a file using pickle
dataS = {"model":regressor, "enc_country":enc_country, "enc_edu":enc_edu}
with open("RModel.pkl","wb") as file:
    pickle.dump(dataS,file)
with open("RModel.pkl","rb") as file:
    dataS = pickle.load(file)

# predicting the data using pickle file that was stored previously above
regressor_loaded = dataS["model"]
enc_country = dataS["enc_country"]
enc_edu = dataS["enc_edu"]
yP = regressor_loaded.predict(X)
print(yP)