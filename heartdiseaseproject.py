# -*- coding: utf-8 -*-
"""HeartDiseaseProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PJPX1xXTZQNybxCzxm76COdB8tB05wUU

**Import the libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import SimpleImputer

#
# %matplotlib inline 
#

"""Read the data"""

data = pd.read_csv("Heart_Disease.csv")

print(data.dtypes)

data.describe()

data.head() # display first 5 rows

"""**draw some plots**"""

data.info()

# select numerical columns
data_numeric = data.select_dtypes(include=['int64', 'float64'])

# select categorical columns
data_categorical = data.select_dtypes(include=['object'])

# calculate mean for each column
imputer = SimpleImputer(strategy='mean')

# replace nulls with mean
data_numeric = pd.DataFrame(imputer.fit_transform(data_numeric), columns=data_numeric.columns)


print(data_numeric)

data_numeric.isnull().sum()

# calculate mode for each column
imputer = SimpleImputer(strategy='most_frequent')

# replace nulls with mode
data_categorical = pd.DataFrame(imputer.fit_transform(data_categorical), columns=data_categorical.columns)

# print the imputed dataframe
print(data_categorical)

data_categorical.isnull().sum()

print (data.duplicated().sum())

data = pd.concat([data_numeric, data_categorical], axis = 1)

data.head()

one_hot = pd.get_dummies(data['smoking_status'], prefix='smoking_status')
data = pd.concat([data, one_hot], axis=1)

one_hot = pd.get_dummies(data['work_type'], prefix='work_type')
data = pd.concat([data, one_hot], axis=1)

one_hot = pd.get_dummies(data['Gender'], prefix='Gender')
data = pd.concat([data, one_hot], axis=1)

one_hot = pd.get_dummies(data['Heart Disease'], prefix='Heart Disease')
data = pd.concat([data, one_hot], axis=1)

# concatenate the one-hot encoded dataframe with the original dataframe

data.head()

# delete old
data.pop('Gender')
data.pop('work_type')
data.pop('smoking_status')
data.pop('Heart Disease')

data.head()

data.head(10)

"""**Rescaling the data**"""

# X_scaled = (X - X_min) / (X_max - X_min)
#rescaling the data from 0 to 1     to have the same weight effect 
scaler = MinMaxScaler()
data[["Age", 'Chest pain type', 'BP', 'Cholesterol', 'FBS over 120', 'EKG results', 'Max HR', 'Exercise angina', 'ST depression', 'Slope of ST', 'Number of vessels fluro', 'Thallium']] = scaler.fit_transform(data[["Age", 'Chest pain type', 'BP', 'Cholesterol', 'FBS over 120', 'EKG results', 'Max HR', 'Exercise angina', 'ST depression', 'Slope of ST', 'Number of vessels fluro', 'Thallium']])

data.head()

sns.boxplot(data['Age'])

sns.boxplot(data['Chest pain type'])

sns.boxplot(data['BP'])

sns.boxplot(data['Cholesterol'])

sns.boxplot(data['FBS over 120'])

sns.boxplot(data['EKG results'])

sns.boxplot(data['Max HR'])

sns.boxplot(data['Exercise angina'])

sns.boxplot(data['ST depression'])

sns.boxplot(data['Slope of ST'])

sns.boxplot(data['Number of vessels fluro'])

sns.boxplot(data['Thallium'])

"""**Replace Outliers with upper whisker and lower whisker**"""

Q1 = data['Chest pain type'].quantile(0.25)
Q3 = data['Chest pain type'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['Chest pain type'] = np.where(data['Chest pain type'] > upper_whisker,upper_whisker,np.where(data['Chest pain type'] < lower_whisker,lower_whisker,data['Chest pain type']))

Q1 = data['BP'].quantile(0.25)
Q3 = data['BP'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['BP']=np.where(data['BP']>upper_whisker,upper_whisker,np.where(data['BP']<lower_whisker,lower_whisker,data['BP']))

Q1 = data['Cholesterol'].quantile(0.25)
Q3 = data['Cholesterol'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['Cholesterol']=np.where(data['Cholesterol']>upper_whisker,upper_whisker,np.where(data['Cholesterol']<lower_whisker,lower_whisker,data['Cholesterol']))

Q1 = data['FBS over 120'].quantile(0.25)
Q3 = data['FBS over 120'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['FBS over 120']=np.where(data['FBS over 120']>upper_whisker,upper_whisker,np.where(data['FBS over 120']<lower_whisker,lower_whisker,data['FBS over 120']))

Q1 = data['Max HR'].quantile(0.25)
Q3 = data['Max HR'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['Max HR']=np.where(data['Max HR']>upper_whisker,upper_whisker,np.where(data['Max HR']<lower_whisker,lower_whisker,data['Max HR']))

Q1 = data['ST depression'].quantile(0.25)
Q3 = data['ST depression'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['ST depression']=np.where(data['ST depression']>upper_whisker,upper_whisker,np.where(data['ST depression']<lower_whisker,lower_whisker,data['ST depression']))

Q1 = data['Number of vessels fluro'].quantile(0.25)
Q3 = data['Number of vessels fluro'].quantile(0.75)
IQR = Q3 - Q1
whisker_width = 1.5
lower_whisker = Q1 - (whisker_width * IQR)
upper_whisker = Q3 + (whisker_width * IQR)

data['Number of vessels fluro']=np.where(data['Number of vessels fluro']>upper_whisker,upper_whisker,np.where(data['Number of vessels fluro']<lower_whisker,lower_whisker,data['Number of vessels fluro']))

corr_matrix = data.corr(method='pearson')[['Heart Disease_Yes', 'Heart Disease_No']]

# print the correlation matrix
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

print(corr_matrix)

corr_matrix = data.corr()

# Plot the heatmap
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.show()

"""****

**Delete columns with small coronation**
"""

# drop columns with correlation less than absolute (0.2)
data = data.drop('id', axis=1)
data = data.drop('BP', axis=1)
data = data.drop('Cholesterol', axis=1)
data = data.drop('FBS over 120', axis=1)
data = data.drop('smoking_status_Unknown', axis=1)
data = data.drop('smoking_status_formerly smoked', axis=1)
data = data.drop('smoking_status_never smoked', axis=1)
data = data.drop('smoking_status_smokes', axis=1)
data = data.drop('work_type_Govt_job', axis=1)
data = data.drop('work_type_Never_worked', axis=1)
data = data.drop('work_type_Private', axis=1)
data = data.drop('work_type_Self-employed', axis=1)
data = data.drop('work_type_children', axis=1)
data = data.drop('Heart Disease_No', axis=1)
data = data.drop('Gender_Male', axis=1)

corr_matrix = data.corr()

# Plot the heatmap
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.show()

data.head()

"""**split the data to features and predictions**"""

x = data.drop(['Heart Disease_Yes'], axis = 1)
y = data['Heart Disease_Yes']

"""split the data to train and test"""

# split 20% to test and 80% to train
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

# Create a Logistic Regression object
logreg = LogisticRegression()

# Fit the model to the training data
logreg.fit(x_train, y_train)

y_pred = logreg.predict(x_test)

# Calculate the accuracy of the model on the test set
accuracy = accuracy_score(y_test, y_pred)

print('Accuracy:', accuracy)
print("Classification Report: \n", classification_report(y_test, y_pred))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
mse = mean_squared_error(y_test.astype('int'), y_pred.astype('int'))
print("Mean Squared Error: ", mse)

# c is hyperparameter determime the penalty for misclassifying data
#  A larger value of C results in a narrower margin, which may reduce misclassifications but can also lead to overfitting.
svm = SVC(kernel='linear', C=1, random_state=42)

svm.fit(x_train, y_train)

y_pred = svm.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)

print('Accuracy:', accuracy)
print("Classification Report: \n", classification_report(y_test, y_pred))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
mse = mean_squared_error(y_test.astype('int'), y_pred.astype('int'))
print("Mean Squared Error: ", mse)

tree = DecisionTreeClassifier(criterion='entropy', max_depth=7, random_state=42)

# Fit the decision tree to the data
tree.fit(x_train, y_train)
y_pred = tree.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report: \n", classification_report(y_test, y_pred))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
mse = mean_squared_error(y_test.astype('int'), y_pred.astype('int'))
print("Mean Squared Error: ", mse)



