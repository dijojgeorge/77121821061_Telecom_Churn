# -*- coding: utf-8 -*-
"""77121821061_Telecom Churn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YjrsQDiTHFYNOlCqck6fN5MC8xj7DjLJ

# **TELECOM CHURN - Classification Project**

Classification for Telecom Churn Analysis

**STEP 1**: Importing dependencies

**STEP 2** : Data collection and pre-processing

**STEP 3** : Splitting the data into training and test sets

**STEP 4** : Feature Extraction : Convert text data into meaningful numerical value

**STEP 5** : Training the Decision Tree / Random Forest Model

**STEP 6** : Evaluvating the trained model - Checking accuracy / Precision on Training data

**STEP 7** : Evaluvating overfitting : Checking accuracy on Test data

**STEP 8** : Building a predictive system

# **STEP 1** : Importing dependencies
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np # to create numpy arrays
import pandas as pd # to create dataframes from CSV file

from sklearn.model_selection import train_test_split # for splitting the data

from sklearn.feature_extraction.text import TfidfVectorizer # to covnert text date into numerical values for ML model understanding
from sklearn.linear_model import LogisticRegression # binary classificaiton
from sklearn.tree import DecisionTreeClassifier # Decision Tree

from sklearn.metrics import accuracy_score # to evaluvate the model's prediction
from sklearn.metrics import precision_score # to evaluvate the precision
from sklearn.metrics import recall_score # to evaluvate the recall
from sklearn.metrics import confusion_matrix # Confusion Matrix
from sklearn.metrics import classification_report # Classification Report

from imblearn.combine import SMOTEENN

import seaborn as sns

import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
# %matplotlib inline

"""# **STEP 2** : Data collection and pre-processing

## Data Loading
"""

# loading data from CSV to Pandas DF
raw_Customer_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Telecom_Chrun/Telco-Customer-Churn.csv')

"""## Basic Check"""

#checking for null values
print(raw_Customer_data)

# replacing the null values with a mull string
Customer_data = raw_Customer_data.where((pd.notnull(raw_Customer_data)),'')

#checking the sample of the DF
Customer_data.head()

# checking the no. of rows and col (size of the df row x col)
Customer_data.shape

# encoding the label to numerical value (ie. Churn yes = 1 and Churn no = 0 to numerical values)
#Customer_data.loc[Customer_data['Churn']=='Yes', 'Churn',]= 1
#Customer_data.loc[Customer_data['Churn']=='No', 'Churn',]= 0

#Customer_data.head() # Checking encoding

Customer_data.dtypes #Checking data types

Customer_data.describe() # to understand the nature of Numerical values parameters

Customer_data['Churn'].value_counts().plot(kind ='barh', figsize = (6,4))
plt.xlabel ("Count", labelpad=14)
plt.ylabel("Target Variable (Churn : Yes = 1 ; No = 0)", labelpad=14)
plt.title("Count of Target Variable per Category", y = 1.02)

100*Customer_data['Churn'].value_counts()/len(Customer_data['Churn']) # To get a high level view of the % distribution

Customer_data['Churn'].value_counts() # To  get a High level distribution of Churn count

Customer_data.info(verbose = True) # To get non null obeject count

"""## Missing Value Check"""

missing = pd.DataFrame((Customer_data.isnull().sum())*100/Customer_data.shape[0]).reset_index() # Finding Missing value %
plt.figure(figsize=(16,5))
ax = sns.pointplot(x='index',y=0, data=missing)
plt.xticks(rotation = 90, fontsize = 7)
plt.title ("Percentage of Missing Values")
plt.ylabel("Percentage")
plt.show()

"""## Data Cleaning"""

Customer_data_copy = Customer_data.copy()

Customer_data_copy.head()

Customer_data_copy.TotalCharges = pd.to_numeric(Customer_data_copy.TotalCharges,errors='coerce')
Customer_data_copy.isnull().sum() # Checking how many Total Charge is null

Customer_data_copy.loc[Customer_data_copy['TotalCharges'].isnull() == True] # Checking the location of null value Total Charges

Customer_data_copy.dropna(how = 'any', inplace = True)
#Customer_data_copy.fillna(0)

print(Customer_data_copy['tenure'].max())

# Creating groups based on tenure spread from 0 to 72
labels = ["{0} - {1}". format(i,i+11) for i in range(1,72,12)]
Customer_data_copy['tenure_group'] = pd.cut(Customer_data_copy.tenure, range(1,80,12), right = False, labels = labels)

Customer_data_copy['tenure_group'].value_counts()

Customer_data_copy.drop(columns = ['customerID','tenure'], axis=1, inplace = True)
Customer_data_copy.head()

"""## Analysis"""

# Univariate Analysis

for i, predictor in enumerate (Customer_data_copy.drop(columns=['Churn', 'TotalCharges', 'MonthlyCharges'])):
  plt.figure(i)
  sns.countplot(data = Customer_data_copy, x=predictor, hue = 'Churn')

Customer_data_copy.head()

Customer_data_copy['Churn'] = np.where(Customer_data_copy.Churn =='Yes', 1,0)
Customer_data_copy.head()

Customer_data_copy_dummies = pd.get_dummies(Customer_data_copy) # Dummy data creation for categorical data
Customer_data_copy_dummies.head()

sns.lmplot(data=Customer_data_copy_dummies, x = 'MonthlyCharges', y = 'TotalCharges',fit_reg = False)

Mth = sns.kdeplot(Customer_data_copy.MonthlyCharges[(Customer_data_copy_dummies["Churn"] == 0)] ,
                  color = "Red", fill  = True)
Mth = sns.kdeplot(Customer_data_copy.MonthlyCharges[(Customer_data_copy_dummies ["Churn"] == 1)] ,
                  ax = Mth, color = "Blue", fill = True)
Mth.legend(["No Churn", "Churn"], loc = 'upper right')
Mth.set_ylabel('Density')
Mth.set_xlabel('Monthly Charges')
Mth.set_title('Monthly charges by churn')

Tot = sns.kdeplot(Customer_data_copy_dummies.TotalCharges[(Customer_data_copy_dummies["Churn"]==0)],
                  color="Red", fill = True)
Tot = sns.kdeplot(Customer_data_copy_dummies.TotalCharges[(Customer_data_copy_dummies["Churn"]==1)],
                  ax = Tot, color="Blue", fill = True)
Tot.legend(["No Churn","Churn"],loc='upper right')
Tot.set_ylabel('Density')
Tot.set_xlabel('Total Charges')
Tot.set_title('Total charges by churn')

plt.figure(figsize=(20,8))
Customer_data_copy_dummies.corr()['Churn'].sort_values(ascending=False).plot(kind='bar')

plt.figure(figsize=(12,12))
sns.heatmap(Customer_data_copy_dummies.corr(),cmap="Paired")

"""**Bivariate Analysis**"""

new_df1_target0=Customer_data_copy.loc[Customer_data_copy["Churn"]==0]
new_df1_target1=Customer_data_copy.loc[Customer_data_copy["Churn"]==1]

def uniplot(df,col,title,hue = None):
  sns.set_style('whitegrid')
  sns.set_context('talk')
  plt.rcParams["axes.labelsize"] = 20
  plt.rcParams["axes.titlesize"] = 22
  plt.rcParams['axes.titlepad'] = 30

  temp = pd.Series(data = hue)
  fig, ax = plt.subplots()
  width = len(df[col].unique())+ 7 + 4*len(temp.unique())
  fig.set_size_inches(width,8)
  plt.xticks(rotation = 45)
  plt.yscale('log')
  plt.title(title)
  ax = sns.countplot(data = df, x = col, order = df[col].value_counts().index,hue = hue, palette = 'bright')

  plt.show()

new_df1_target1.head()

uniplot(new_df1_target0,col='Partner',title = 'Dist of Gender for Non Customer Churn', hue = 'gender')

uniplot(new_df1_target1,col='PaymentMethod',title = 'Dist of Payment Method for Customer Churn', hue = 'gender')

uniplot(new_df1_target1,col='Contract',title = 'Dist of Contract for Customer Churn', hue = 'gender')

uniplot(new_df1_target1,col='TechSupport',title = 'Dist of Gender for Customer Churn', hue = 'gender')

uniplot(new_df1_target1,col='SeniorCitizen',title = 'Dist of Gender for Customer Churn', hue = 'gender')

Customer_data_copy_dummies.to_csv('Customer_churn.csv')

"""# STEP 3 : Splitting the data into training and test sets

## Loading data. Creating X and Y variable
"""

df = pd.read_csv('Customer_churn.csv')

df.head(5)

df = df.drop('Unnamed: 0', axis =1)

df.head(5)

x = df.drop('Churn', axis =1)
x

y = df['Churn']
y

"""## Spliting Data into train and test set"""

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2)

"""# STEP 4 : Model 1 : Decision Tree"""

model_dt=DecisionTreeClassifier(criterion='gini', random_state=100, max_depth=6, min_samples_leaf=8)

model_dt.fit(x_train, y_train) # fitting the data

y_pred = model_dt.predict(x_test)

y_pred

model_dt.score(x_test,y_pred)

print(classification_report(y_test, y_pred, labels =[0,1]))

print(confusion_matrix(y_test, y_pred))

"""## SMOOTEENN (edited Nearnest Neighbour) for balancing the data"""

sm = SMOTEENN()
X_resampled, y_resampled = sm.fit_resample(x,y)

xr_train, xr_test, yr_train, yr_test = train_test_split(X_resampled, y_resampled, test_size = 0.2)

model_dt_smote = DecisionTreeClassifier(criterion = 'gini', random_state=100, max_depth=6, min_samples_leaf =8)

model_dt_smote.fit(xr_train, yr_train)

y_pred_smote = model_dt_smote.predict(xr_test)

print(classification_report(yr_test, y_pred_smote, labels =[0,1]))

print(confusion_matrix(yr_test, y_pred_smote))

"""# STEP 5 : Model 2 : Random Forest"""

from sklearn.ensemble import RandomForestClassifier

model_rf=RandomForestClassifier (n_estimators= 100, criterion = 'gini', random_state = 100, max_depth =6, min_samples_leaf=8)

model_rf.fit(x_train, y_train) # fitting the data

y_pred_rf = model_rf.predict(x_test)

y_pred_rf

model_rf.score(x_test,y_pred_rf)

print(classification_report(y_test, y_pred_rf, labels =[0,1]))

print(confusion_matrix(y_test, y_pred_rf))

"""## SMOOTEENN (edited Nearnest Neighbour) for balancing the data"""

sm = SMOTEENN()
X_resampled, y_resampled = sm.fit_resample(x,y)

xr_train, xr_test, yr_train, yr_test = train_test_split(X_resampled, y_resampled, test_size = 0.2)

model_rf_smote = RandomForestClassifier (n_estimators= 100, criterion = 'gini', random_state = 100, max_depth =6, min_samples_leaf=8)

model_rf_smote.fit(xr_train, yr_train)

y_pred_smote_rf = model_rf_smote.predict(xr_test)

print(classification_report(yr_test, y_pred_smote_rf, labels =[0,1]))

print(confusion_matrix(yr_test, y_pred_smote_rf))



"""# STEP 6 : Model 2 : Random Forest (TO CHANGE)"""

from sklearn.ensemble import RandomForestClassifier

model_rf=RandomForestClassifier (n_estimators= 100, criterion = 'gini', random_state = 100, max_depth =6, min_samples_leaf=8)

model_rf.fit(x_train, y_train) # fitting the data

y_pred_rf = model_rf.predict(x_test)

y_pred_rf

model_rf.score(x_test,y_pred_rf)

print(classification_report(y_test, y_pred_rf, labels =[0,1]))

print(confusion_matrix(y_test, y_pred_rf))

"""## SMOOTEENN (edited Nearnest Neighbour) for balancing the data"""

sm = SMOTEENN()
X_resampled, y_resampled = sm.fit_resample(x,y)

xr_train, xr_test, yr_train, yr_test = train_test_split(X_resampled, y_resampled, test_size = 0.2)

model_rf_smote = RandomForestClassifier (n_estimators= 100, criterion = 'gini', random_state = 100, max_depth =6, min_samples_leaf=8)

model_rf_smote.fit(xr_train, yr_train)

y_pred_smote_rf = model_rf_smote.predict(xr_test)

print(classification_report(yr_test, y_pred_smote_rf, labels =[0,1]))

print(confusion_matrix(yr_test, y_pred_smote_rf))

"""# Step 7 :Naive Bayes Model (TO UPDATE)"""





"""# STEP X : Saving the model

## Random forest
"""

import pickle
from google.colab import drive
drive.mount('/content/drive')
pick_insert = open('/content/drive/My Drive/Colab Notebooks/Telecom_Chrun/model_rf.pkl','wb')
#pick_insert = open('/content/drive/My Drive/Colab Notebooks/Telecom_Chrun/model_rf.pkl','wb')
pickle.dump(model_rf_smote, pick_insert)

load_model = pickle.load(open('/content/drive/My Drive/Colab Notebooks/Telecom_Chrun/model_rf.pkl', 'rb'))

load_model.score(xr_test, yr_test)