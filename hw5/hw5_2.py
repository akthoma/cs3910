#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================
Homework 5.2
@author: huntercarver
edits by audreytinkey
=================
"""

import pandas as pd

from sklearn import preprocessing as pp
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict

# Won't show copy warning
pd.options.mode.chained_assignment = None

# read in data into pandas dataframe
health = pd.read_csv('hw5data/HealthInsuranceClean.csv',
                     na_values='Null')

# Fill all Null values with the previous value
health.fillna(method='bfill', inplace=True)
# Print after null conversion
print(health.head())

export_csv = health.to_csv('hw5data/fixedhw5_2.csv', index=None, header=True)

# Convert Coverage types to Dummy Variables in own DF
Coverage = pd.get_dummies(health['Coverage Type'])
# Sanity Check
# print(Coverage.head())

# Combine the separate dataframes through concatenation
health = health.merge(Coverage, left_index=True, right_index=True)
# print(health.head())

# Convert Income types to Dummy Variables in own DF
Income = pd.get_dummies(health['Family Income'])
# Sanity Check
# print(Income.head())

# Combine the separate dataframes through concatenation
health = health.merge(Income, left_index=True, right_index=True)
# print(health.head())

# Convert Age types to Dummy Variables in own DF
Age = pd.get_dummies(health['Age'])
# Sanity Check
# print(Age.head())

# Combine the seperate dataframes through concatanation
health = health.merge(Age, left_index=True, right_index=True)
# print(health.head())

# Convert Location types to Dummy Variables in own DF
Location = pd.get_dummies(health['Location'])
# Sanity Check
# print(Location.head())

# Combine the seperate dataframes through concatanation
health = health.merge(Location, left_index=True, right_index=True)
# print(health.head())

# Convert Location types to Dummy Variables in own DF
# DataType = pd.get_dummies(health['Data Type'])
# Sanity Check
# print(DataType.head())

# Combine the seperate dataframes through concatanation
# health = health.merge(DataType, left_index=True, right_index=True)
# print(health.head())

# Print all columns name for Reference
# print(health.columns.tolist())

# Dropping Columns that we converted to dummy variables
health.drop(['Fips', 'Location', 'Coverage Type', 'Family Income', 
             'Age'], axis=1, inplace=True)

# Printing Results before Scaling but after dummy variables set
print(health.head())

# Making a list of all columns to scale
columns = ['TimeFrame', 'Percent', 'MOE', 'Number', 'Employer', 'Individual', 'Insured', 'Medicaid/CHIP', 'Medicare',
           'Private', 'Public', 'Uninsured', '$25,000 - $49,999', '$50,000 - $74,999', '$75,000 or more',
           'Under $25,000', '0-18', '0-64', '19-25', '19-64', '65+', 'Alabama', 'Alaska', 'Arizona', 'Arkansas',
           'California', 'Colorado', 'Connecticut', 'Delaware', 'Dist. of Columbia', 'Florida', 'Georgia', 'Hawaii',
           'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
           'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
           'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
           'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
           'Texas', 'United States', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin',
           'Wyoming']

# Intialize Scale
scale = pp.MinMaxScaler()

# Apply our scaling functon to our dataframe
health[columns] = scale.fit_transform(health[columns])

# Print after Scaling
print(health.head())

# Dropping all rows with null values to make similar size
no_nulls = health.dropna(how='any')
health = health.dropna(how='any')

y = no_nulls['Percent']

# Split model into test and train data
x_Train, x_Test, y_Train, y_Test = train_test_split( 
        health, y, test_size=0.2)

print(x_Train.shape, y_Train.shape)
print(x_Test.shape, y_Test.shape)

# Fit the model close to the LinearRegression line
lm = linear_model.LinearRegression()
# Create or model based off of our training data
Model = lm.fit(x_Train, y_Train)
# Make cross_val_predictions with 6 K-Folds Cross Validation
Percent_predictions = cross_val_predict(Model, health, y, cv=6)
# Show our first 5 Model predictions
print(Percent_predictions[0:5])

y = no_nulls['MOE']

# Split model into test and train data
x_Train, x_Test, y_Train, y_Test = train_test_split( 
        health, y, test_size=0.2)

print(x_Train.shape, y_Train.shape)
print(x_Test.shape, y_Test.shape)

# Fit the model close to the LinearRegression line
lm = linear_model.LinearRegression()
# Create or model based off of our training data
Model = lm.fit(x_Train, y_Train)
# Make cross_val_predictions with 6 K-Folds Cross Validation
MOE_predictions = cross_val_predict(Model, health, y, cv=6)
# Show our first 5 Model predictions
print(MOE_predictions[0:5])

y = no_nulls['Number']

# Split model into test and train data
x_Train, x_Test, y_Train, y_Test = train_test_split(
        health, y, test_size=0.2)

print(x_Train.shape, y_Train.shape)
print(x_Test.shape, y_Test.shape)

# Fit the model close to the LinearRegression line
lm = linear_model.LinearRegression()
# Create or model based off of our training data
Model = lm.fit(x_Train, y_Train)
# Make cross_val_predictions with 6 K-Folds Cross Validation
Number_predictions = cross_val_predict(Model, health, y, cv=6)
# Show our first 5 Model predictions
print(Number_predictions[0:5])

# read in original data into pandas dataframe
finalHealth = pd.read_csv('hw5data/HealthInsuranceClean.csv',
                          na_values='Null')

# Convert our numpy arrays to a dataFrame to add to our original DF
Percent_predictions = pd.DataFrame(data=Percent_predictions.flatten())
MOE_predictions = pd.DataFrame(data=MOE_predictions.flatten())
Number_predictions = pd.DataFrame(data=Number_predictions.flatten())
# Renaming Columns of DataFrame for later functionality
Percent_predictions.columns = ['Percent']
MOE_predictions.columns = ['MOE']
Number_predictions.columns=['Number']

# Sanity Check on current DataFrame Columns
print(Percent_predictions.head())
print(MOE_predictions.head())
print(Number_predictions.head())

print(finalHealth.head())
# Add our new Percent predictions to na Values in Percent Col
finalHealth.Percent = finalHealth.Percent.fillna(value=Percent_predictions.Percent)
print(finalHealth.head())
# Add our new MOE predictions to na values in MOE Col
print(finalHealth.head())
finalHealth.MOE = finalHealth.MOE.fillna(value=MOE_predictions.MOE)
print(finalHealth.head())
# Add our new Number predictions to na values in Number Col
finalHealth.Number = finalHealth.Number.fillna(value=Number_predictions.Number)
print(finalHealth.head())

# Write updated Final Dataframe to CSV
export_csv = finalHealth.to_csv('hw5data/fixedhw5_2.csv', index=None, header=True)
