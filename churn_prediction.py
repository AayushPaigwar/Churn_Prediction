# -*- coding: utf-8 -*-
"""Churn_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bI7bGMMVFOuMLvtPhllylMNuN2AHZehM
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

data_churn= pd.read_csv("/content/churn_data.csv")
data_churn.head(10)

data_churn.columns.values

data_churn.dtypes

data_churn.TotalCharges = pd.to_numeric(data_churn.TotalCharges, errors='coerce')
data_churn.isnull().sum()  #number of null values

#Removing missing values
data_churn.dropna(inplace = True)

#Customer ID removing
df=data_churn.iloc[:,1:]

#converting the predictor variable in binary form(0,1)

df['Churn'].replace(to_replace='Yes', value=1, inplace= True)
df['Churn'].replace(to_replace='No', value=0,inplace= True)
df['Churn'].head()

#converting all the categorial variable into dummy variables
df_dummy= pd.get_dummies(df)
df_dummy.head()

df_dummy.dtypes

"""#Performing **Exploratory Data Analysis(EDA)**"""

#get correlation of the churn with other variables
plt.figure(figsize=(15,8))
df_dummy.corr()['Churn'].sort_values(ascending= False).plot(kind= 'bar')

"""##**Gender Distribution**"""

colors =['red','purple']
gen= (data_churn['gender'].value_counts()*100.0 / len(data_churn)).plot(kind= 'bar', stacked= True, rot= 0, color=colors)
gen.yaxis.set_major_formatter(mtick.PercentFormatter())
gen.set_ylabel('Customers %')
gen.set_xlabel('Gender')
gen.set_title('Gender Distribution %')

total=[]

for i in gen.patches:
  total.append(i.get_width())

total=sum(total)

for i in gen.patches:
  gen.text(i.get_x()+.15,i.get_height()-3.5, str(round((i.get_height()/total),1))+'%', fontsize=12, color='white',weight= 'bold' )

"""##**Senior Citizens**"""

gen =(data_churn['SeniorCitizen'].value_counts()*100.0/ len(data_churn)).\
plot.pie(autopct='%.1f%%', labels= ['Yes', 'No'], figsize=(5,5) , fontsize= 10)
gen.set_title('Senior Citizen %', fontsize= 10)
gen.set_ylabel('Senior Citiizens', fontsize=10)

"""##**Dependant and Independant partner**"""

df2 = pd.melt(data_churn, id_vars=['customerID'], value_vars=['Dependents','Partner'])
df3= df2.groupby(['variable','value']).count().unstack()
df3= df3*100/len(data_churn)
gen= df3.loc[:,'customerID'].plot.bar(stacked=True, color=colors, figsize=(8,6),rot=0,width= 0.2)

gen.yaxis.set_major_formatter(mtick.PercentFormatter())
gen.set_ylabel( 'Customers %', size=12)
gen.set_xlabel('')
gen.set_title('Customers % with Dependent and partner')
gen.legend(loc='center',prop={'size':12})

for j in gen.patches:
  width,height= j.get_width(),j.get_height()
  x,y=j.get_xy()
  gen.annotate('{:.0f}%'.format(height),(j.get_x()+.25*width,j.get_y()+.4*height),\
                 color = 'white',weight='bold',size=10)

"""##**Tenure**"""

gen= sns.distplot(data_churn['tenure'],hist=True,kde=False,
             bins=int(180/5),color= 'blue',
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth':10})

"""##**Number of Contracts**"""

gen = data_churn['Contract'].value_counts().plot(kind = 'bar', rot = 0, width = 0.3)
gen.set_ylabel('Number of Customers')
gen.set_xlabel('Contract type')

"""##**Separate Contracts (Month-to-month, 1 year , 2 year)**"""

fig,(ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3,sharey=True, figsize=(20,6))

ax = sns.distplot(data_churn[data_churn['Contract']== 'Month-to-month']['tenure'],
                  hist=True ,kde= False,
                  bins= int(180/5),color='orange',
                  hist_kws={'edgecolor':'black'},
                  kde_kws={'linewidth':4},
                  ax=ax1)
ax.set_ylabel('Number of Customer')
ax.set_xlabel('Tenure(months)')
ax.set_title('Month-to-month Contract')

ax= sns.distplot(data_churn[data_churn['Contract']=='One year']['tenure'],
                 hist=True, kde=False,
                 bins=int(180/5),color='red',
                 hist_kws={'edgecolor':'black'},
                 kde_kws={'lineiwidth':4},
                 ax=ax2)
ax.set_ylabel('Number of Customer')
ax.set_xlabel('Tenure(months)')
ax.set_title('One year Contract')

ax= sns.distplot(data_churn[data_churn['Contract']=='Two year']['tenure'],
                 hist=True, kde=False,
                 bins=int(180/5),color='blue',
                 hist_kws={'edgecolor':'black'},
                 kde_kws={'lineiwidth':4},
                 ax=ax3)
ax.set_ylabel('Number of Customer')
ax.set_xlabel('Tenure(months)')
ax.set_title('Two year Contract')

"""##**List of services used by customers**"""

data_churn.columns.values

services =['PhoneService', 'MultipleLines','InternetService','OnlineSecurity','OnlineBackup','DeviceProtection',
           'TechSupport','StreamingTV','StreamingMovies']

"""##**Monthly & Total Charges**"""

data_churn[['MonthlyCharges','TotalCharges']].plot.scatter(x='MonthlyCharges', y='TotalCharges', color='red')

"""##**Churn Rate**"""

colors = ['red','blue']
ax= (data_churn['Churn'].value_counts()*100.0/len(data_churn)).plot(kind='bar',
                                                                    stacked= True,
                                                                    rot =0,
                                                                    color=colors,
                                                                    figsize= (8,6))
ax.yaxis.set_major_formatter(mtick.PercentFormatter()),
ax.set_title('Churn Rate %'),
ax.set_xlabel('Churn',size=12),
ax.set_ylabel('Customer %',size=12)

#List to collect the Churn rate(1,0)
total=[]

# adding all churn data in 'total'
for k in ax.patches:
  total.append(k.get_width())

total=sum(total)

# get_x used to moves left & right
# get_y used to move up & down
for k in ax.patches:
  ax.text(k.get_x()+.15, k.get_height()-5.0,\
          str(round((k.get_height()/total),1))+'%',
          fontsize=15, color='white',weight= 'bold')

"""## **Comparision between Churn & Tenure**"""

sns.boxplot(x= data_churn.Churn, y = data_churn.tenure)

"""## **Churn according to monthly charges**"""

ax= sns.kdeplot(data_churn.MonthlyCharges[(data_churn['Churn']== 'No')],
                color='Red',shade=True)
ax= sns.kdeplot(data_churn.MonthlyCharges[(data_churn['Churn']=='Yes')],
                color = 'Blue',shade= True)

ax.set_title('Churn according to Monthly Charges')
ax.legend(['Not Churn','Churn'],loc='upper right')
ax.set_ylabel('Density')

"""## **After doing the EDA we are going to develop Logistic Regression Model**"""

x= df_dummy.drop(columns =['Churn'])
y= df_dummy['Churn'].values

#Scaling all the variables to range 0 to 1
from sklearn.preprocessing import MinMaxScaler
features = x.columns.values
scaler = MinMaxScaler(feature_range = (0,1))
scaler.fit(x)
x=pd.DataFrame(scaler.transform(x))
x.columns = features

#Creating test and train model
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3, random_state=42)

#Running Logistic Regression Model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
result= model.fit(x_train,y_train)

from sklearn import metrics
prediction_test = model.predict(x_test)
print(metrics.accuracy_score(y_test,prediction_test))

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
y_pred = result.predict(x_test)
print("Accuracy Score:", accuracy_score(y_test,y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test,y_pred))

print("Classification report:")
print(classification_report(y_test,y_pred))
