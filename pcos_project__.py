# -*- coding: utf-8 -*-
"""PCOS_Project_ .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R__fVeLiqGTEzQGMgUJYZ_kURL68u6xr
"""

from google.colab import drive
drive.mount('/content/drive')

#importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#reading dataset
df=pd.read_csv("/content/drive/MyDrive/datasets(1)/PCOS_data_without_infertility.xlsx - Full_new.csv")

df.info()

df.head()

#df["BMI"]=(df["Weight (Kg)"])/(df["Height(Cm)"]*df["Height(Cm)"]*0.0001)
#df["Waist:Hip Ratio"]=df["Waist(inch)"]/df["Hip(inch)"]
#df["FSH/LH"]=df["FSH(mIU/mL)"]/df["LH(mIU/mL)"]

#checking null values in dataset
df.isnull().sum()

#the rows with null values are droped
df.dropna(axis=0,inplace=True)

df.isnull().sum()

#checking for duplicate rows
df.duplicated().sum()

#droping duplicates if any
df.drop_duplicates()

#droping unnecessay columns
df.drop(["Sl. No","Patient File No."],axis=1,inplace=True)

#correcting incorrect data
df.loc[df["II    beta-HCG(mIU/mL)"]=="1.99."]

df.at[123,"II    beta-HCG(mIU/mL)"]=1.99

df["II    beta-HCG(mIU/mL)"].loc[df.index[123]]

df.loc[df["AMH(ng/mL)"]=="a"]

df.drop(305,axis=0,inplace=True)

#datatype handling
df['II    beta-HCG(mIU/mL)']=df['II    beta-HCG(mIU/mL)'].astype(float)
df['AMH(ng/mL)']=df['AMH(ng/mL)'].astype(float)

df.info()

#categorical features
cat_col=list(df.columns[df.nunique()==2])

cat_col.append("Blood Group")

print(cat_col)

#numerical features
num_col = [x for x in list(df.columns) if x not in cat_col]

print(num_col)

"""**UNIVARIATE ANALYSIS**"""

#histogram
df[num_col].hist(bins=40,figsize=(50,50))
plt.show()

#distribution plot
plt.figure(figsize=[20,20])
plt.suptitle("Univariate Analysis of Numerical Features :")
for i in range(0,len(num_col)):
  plt.subplot(6,6,i+1)
  sns.kdeplot(x=df[num_col[i]],shade=True)

#boxplot
plt.figure(figsize=[20,20])
plt.suptitle("Outliers in Numerical Features :")
for i in range(0,len(num_col)):
  plt.subplot(6,6,i+1)
  sns.boxplot(x=df[num_col[i]])

#correlation matrix
df.corr()

#correlation heatmap
fig, ax = plt.subplots(figsize=(60,60))
sns.heatmap(df.corr(),cmap="CMRmap", annot=True,linewidths=.5,ax=ax)
plt.show()

#to get highly correlated features
numeric = df[num_col]
correlation = numeric.corr()
high_corr=[]

for c1 in num_col:
  for c2 in num_col:
    if c1 != c2 and c2 not in high_corr and correlation[c1][c2] > 0.98:
      high_corr.append(c1)

#no features have correlation higher than 0.98
high_corr

#x-independent features y-dependent features
x=df.iloc[:,:-1].values
y=df.iloc[:,-1].values

plt.hist(y)
plt.show()

"""means the dataset is unbalanced"""

#train test splitting
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=0.25, random_state=0)

#standardisation
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train = sc.transform(X_train)
X_test = sc.transform(X_test)

#principal component analysis
from sklearn.decomposition import PCA
pca = PCA(n_components = 0.95)

X_new_train = pca.fit_transform(X_train)
X_new_test = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_

len(X_new_train[0])

"""number of features reduced to 33"""

fig, axes = plt.subplots(1,2)
axes[0].scatter(X_train[:,0], X_train[:,1], c=y_train)
axes[0].set_xlabel('x1')
axes[0].set_ylabel('x2')
axes[0].set_title('Before PCA')
axes[1].scatter(X_new_train[:,0], X_new_train[:,1], c=y_train)
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
axes[1].set_title('After PCA')
plt.show()

"""**LOGISTIC REGRESSION (BEFORE SMOTE)**"""

#logistic regression
from sklearn.linear_model import LogisticRegression  
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_new_train, y_train)

y_pred = classifier.predict(X_new_test)

#evaluation metrics
from sklearn.metrics import confusion_matrix,accuracy_score,f1_score
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(2,2))
sns.heatmap(cm, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy : ",accuracy_score(y_test,y_pred))
print("\nF1 score : ",f1_score(y_test,y_pred))

"""**LOGISTIC REGRESSION (AFTER SMOTE)**

balancing data using smote (oversampling)
"""

from imblearn.over_sampling import SMOTE
smote = SMOTE(sampling_strategy='not majority')
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=0.25, random_state=0)
X_train, y_train = smote.fit_resample(X_train, y_train)

plt.hist(y_train)
plt.show()

#standardization and pca
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_train = sc.transform(X_train)
X_test = sc.transform(X_test)
from sklearn.decomposition import PCA
pca = PCA(n_components = 0.95)

X_new_train = pca.fit_transform(X_train)
X_new_test = pca.transform(X_test)
  
explained_variance = pca.explained_variance_ratio_

len(X_new_train[0])

#logistic regression
from sklearn.linear_model import LogisticRegression  
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_new_train, y_train)
y_pred = classifier.predict(X_new_test)
from sklearn.metrics import confusion_matrix,accuracy_score,f1_score
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(2,2))
sns.heatmap(cm, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred))
print("\nF1 score after smote : ",f1_score(y_test,y_pred))

"""**RANDOM FOREST**"""

from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier()
rf.fit(X_new_train,y_train)

y_pred_rf = rf.predict(X_new_test)

from sklearn import metrics 
cm_rf=metrics.confusion_matrix(y_test,y_pred_rf)
plt.figure(figsize=(2,2))
sns.heatmap(cm_rf, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred_rf))
print("\nF1 score after smote : ",f1_score(y_test,y_pred_rf))

"""**DECISION TREE**"""

from sklearn.tree import DecisionTreeClassifier
dt=DecisionTreeClassifier()
dt.fit(X_new_train,y_train)

y_pred_dt = dt.predict(X_new_test)

from sklearn import metrics 
cm_dt=metrics.confusion_matrix(y_test,y_pred_dt)
plt.figure(figsize=(2,2))
sns.heatmap(cm_dt, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred_dt))
print("\nF1 score after smote : ",f1_score(y_test,y_pred_dt))

"""**SVM**"""

from sklearn.svm import SVC
svc=SVC(random_state=0)
svc.fit(X_new_train,y_train)

y_pred_svc = svc.predict(X_new_test)

from sklearn import metrics 
cm_svc=metrics.confusion_matrix(y_test,y_pred_svc)
plt.figure(figsize=(2,2))
sns.heatmap(cm_svc, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred_svc))
print("\nF1 score after smote : ",f1_score(y_test,y_pred_svc))

svc1=SVC(kernel="rbf",C=100,gamma=0.001,random_state=0)
svc1.fit(X_new_train,y_train)
y_pred_svc1 = svc1.predict(X_new_test)
from sklearn import metrics 
cm_svc1=metrics.confusion_matrix(y_test,y_pred_svc1)
plt.figure(figsize=(2,2))
sns.heatmap(cm_svc1, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred_svc1))
print("\nF1 score after smote : ",f1_score(y_test,y_pred_svc1))

"""**SVM HYPERTUNING**"""

svc1=SVC(kernel="rbf",C=100,gamma=0.001,random_state=0)
svc1.fit(X_new_train,y_train)
y_pred_svc1 = svc1.predict(X_new_test)
from sklearn import metrics 
cm_svc1=metrics.confusion_matrix(y_test,y_pred_svc1)
plt.figure(figsize=(2,2))
sns.heatmap(cm_svc1, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
plt.show()
print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred_svc1))
print("\nF1 score after smote : ",f1_score(y_test,y_pred_svc1))

#svc2=SVC(kernel="linear")
#svc2.fit(X_new_train,y_train)
#y_pred_svc2 = svc2.predict(X_new_test)
#from sklearn import metrics 
#cm_svc2=metrics.confusion_matrix(y_test,y_pred_svc2)
#plt.figure(figsize=(2,2))
#sns.heatmap(cm_svc2, annot=True, linewidths=1, square = True, cmap = 'Blues_r')
#plt.show()
#print("\nAccuracy after smote : ",accuracy_score(y_test,y_pred_svc2))
#print("\nF1 score after smote : ",f1_score(y_test,y_pred_svc2))

