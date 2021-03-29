# -*- coding: utf-8 -*-
"""
data_cleaning.py
Mia Ma
3/26/2021
clean the data for the Data Analyst Project
"""
#load pakages
import pandas as pd

#read the data
df = pd.read_csv('DataAnalyst.csv')
#drop n/a NaN rows, 1 row is removed from 2252 rows 
df = df.dropna()

#--------------------------------------------salary
#original data: $37K-$66K (Glassdoor est.)
#cleaned data:  37-66
#added col: min, max, average

#remove any row that has '-1' in its salary col
df = df[df['Salary Estimate'] != '-1']

#get rid of the '(Glassdoor est.)' postfix in the salary col
#apply function lambda to every row in the ''Salary Estimate' col
#string.split(seperator = whitespace, maxsplit = -1) 
#--> a list of strings(splited)
#[0] because we only want the first item of the returned list
#which is everything before the seperator
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]) 

#remove the 'K' and the '$'
#	$37K-$66K  --> 37-66
minus_KD = salary.apply(lambda x: x.replace('K','').replace('$',' '))

#to create a new col in a dataframe
#df['name of new col'] = ...

# salary estimate: min - max
df['Min_Salary'] = minus_KD.apply(lambda x: int(x.split('-')[0]))
# df['Min_Salary'].dtype --> to check the datatype
df['Max_Salary'] = minus_KD.apply(lambda x: int(x.split('-')[1]))
# df['Max_Salary'].dtype
#take the average between min and max
df['Ave_Salary'] = (df.Min_Salary + df.Max_Salary) / 2

#---------------------------------------------company name
#remove the rating after each name

#some have ratings at the end, some don't.
#some have '()' ',' '.' in their names
#rating's form is consistent, x.x at the end, 3 char at the end    
#if there is no rating after the name, that row's 'Rating' col will be -1
#to apply this every row in df, use 'axis = 1'
df['Company_Name_Text'] = df.apply(lambda x: 
                                   x['Company Name'] 
                                   if x['Rating'] < 0 
                                   else x['Company Name'][:-3], 
                                   axis = 1)
    

    
#remove the new line character
df['Company_Name_Text'] = df.Company_Name_Text.apply(lambda x: x.replace('\n', ''))

#-----------------------------------------------state of location
#Location: Fairfield, NJ
#State: NJ
#Headquarter_Position: =1 if this position is at Headquarters else =0

#only want the state initials
df['State'] = df['Location'].apply(lambda x: x.split(',')[-1])
#count distinct values --> return from most to least:
#df.State.value_counts()

df['Headquarter_Position'] = df.apply(lambda x: 
                                      1 
                                      if x['Headquarters'] == x['Location']
                                      else 0,
                                      axis = 1)

#-----------------------------------------------age of company
#age = present - 'Founded'
#some companies are missing founded year, which will be -1
df['Company_age'] = df['Founded'].apply(lambda x: 
                                        2021 - x
                                        if x > 0
                                        else -1)
    
#----------------------------------------------parsing job descriptions
df['Python'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'python' in x.lower()
                                           else 0)
#df.Python.value_counts()

#This is not useful because people usually just say 'R'
#but we cannot search 'R', it might not be accurate
df['R_Studio'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'r studio' in x.lower()
                                               or 'r-studio' in x.lower()
                                           else 0)
#df.R_Studio.value_counts()

df['SQL'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'SQL' in x
                                           else 0)
#df.SQL.value_counts()

df['Excel'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'excel' in x.lower()
                                           else 0)
#df.Excel.value_counts()


df['Machine_Learning'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'machine learning' in x.lower()
                                           else 0)
#df.Machine_Learning.value_counts()

df['Tableau'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'tableau' in x.lower()
                                           else 0)
#df.Tableau.value_counts()

df['AWS'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'aws' in x.lower()
                                               or 'amazon web services' in x.lower()
                                           else 0)
#df.AWS.value_counts()

df['Spark'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'spark' in x.lower()
                                           else 0)
#df.Spark.value_counts()

df['Google_Analytics'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'google analytics' in x.lower()
                                           else 0)
#df.Google_Analytics.value_counts()

df['Power_BI'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'powerbi' in x.lower()
                                           else 0)
#df.Power_BI.value_counts()

df['Big_Query'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'bigquery' in x.lower()
                                           else 0)
#df.Big_Query.value_counts()

df['Looker'] = df['Job Description'].apply(lambda x: 
                                           1 
                                           if 'looker' in x.lower()
                                           else 0)
#df.Looker.value_counts()

#------------------------------------------------job titles
def Title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
    
df['Job_Simp'] = df['Job Title'].apply(Title_simplifier)
#df.Job_simp.value_counts()
    
#------------------------------------------------seniority
def Seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'
    
df['Seniority'] = df['Job Title'].apply(Seniority)
#df.Seniority.value_counts()

#------------------------------------------------num of competitors
df['Num_Comp'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)
#df.Num_Comp.value_counts()

#---------------------------------------------remove useless 1st col
#df.columns() --> names of all col
df_cleaned = df.drop(['Unnamed: 0'], axis = 1)  

#---------------------------------------------output
#index = False to avoid the indes col
df_cleaned.to_csv('DataAnalyst_Cleaned.csv', index = False)

#to check if output succcessful:
#pd.read_csv('DataAnalyst_Cleaned.csv')