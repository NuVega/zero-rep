import pandas as pd

df = pd.read_csv('student_depression_dataset.csv')
print(df.head())
print(df.info())
print(df.describe())

dz = pd.read_csv('dz.csv')
print(dz.head())

group = dz.groupby('City')['Salary'].mean()
print(group)