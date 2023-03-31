# Data cleaning and feature engineering 


# Working directory 

import os
os.chdir(r'C:\Users\prajw\OneDrive\Desktop\ds_salary_project')


# Import the libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')
# Load the data

data = pd.read_csv('glassdoor_jobs.csv')
data.head()
# check the shape of the data

data.shape
# check the info of the data

data.info()
# check the null values

data.isnull().sum()
# describe the data

data.describe()

''' 
(Potential issues with data). 

- Parse the salary estimate festure.
- Remove numbers from company name.
- Age of company.
- Parse the job description.
- Parse the State. 

'''

# salary estimate parsing 

data['hourly'] = data['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
data ['employer_provided'] = data ['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

data  = data [data ['Salary Estimate'] != '-1']
salary = data ['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))


# min and max salary 

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

data ['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
data ['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
data ['avg_salary'] = (data .min_salary+data .max_salary)/2


# Company name text only

data ['company_txt'] = data .apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3], axis = 1)


# state field 

data ['job_state'] = data ['Location'].apply(lambda x: x.split(',')[1])
data .job_state.value_counts()

data ['same_state'] = data .apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)


# age of company 

data ['age'] = data .Founded.apply(lambda x: x if x <1 else 2020 - x)


# python

data ['python_yn'] = data ['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)


# R studio 

data ['R_yn'] = data ['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
data .R_yn.value_counts()


# Spark 

data ['spark'] = data ['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
data .spark.value_counts()


# AWS
 
data ['aws'] = data ['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
data .aws.value_counts()


# Excel

data ['excel'] = data ['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
data .excel.value_counts()

data .columns

data_out = data .drop(['Unnamed: 0'], axis =1)

data_out.to_csv('salary_data_cleaned.csv',index = False)


# cleaned data

data.drop(['Unnamed: 0'], axis =1, inplace = True)
data.head()
