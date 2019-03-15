import pandas as pd

# don't show copy warning
pd.options.mode.chained_assignment = None

# read in the data to pandas dataframe
mar = pd.read_csv('hw5data/MarriageClean.csv',
                  header=0,
                  na_values='Null',
                  index_col=None)

div = pd.read_csv('hw5data/DivorceClean.csv',
                  header=0,
                  na_values='Null',
                  index_col=None)

df = div.merge(mar, how='outer')

df.to_csv(path_or_buf='hw5data/mergedhw5_1.csv',
          na_rep='Null',
          index=False)

# covert null values into a list
null_list = df.index[df.isnull().any(axis=1) == True].tolist()


# print all null values
def printmissing(dataframe, name):
    print(name+":\n", dataframe.iloc[null_list], '\n')


printmissing(df, "original null values")
# print a summary of all the null values
print("number of null values in the dataframe:\n", df.isna().sum(), '\n')


# get a new dataframe with only values for Colorado
co_fix = df.loc[df['State'] == 'Colorado']

# use LOCF method to fill the missing value
co_fix.fillna(method='bfill',inplace=True)

# fill the values to original dataframe
df = df.fillna(co_fix)


# get a new dataframe with only values for Indiana
indiana_fix = df.loc[df['State'] == 'Indiana']

# drop all of the columns except for divorce rate
indiana_fix.drop(['Marriage rate', 'Year'], axis=1, inplace=True)

# calculate the mean divorce rate for a subset of data containing only Ohio and Illinois.
mean_div = df['divorce_rate'].loc[df['State'].isin(['Ohio', 'Illinois'])].mean()

# set all of the divorce rates in indiana_fix to be the mean of both Ohio and Illinois
indiana_fix['divorce_rate'] = mean_div

# fill the values to original dataframe
df.fillna(indiana_fix, inplace=True)

# printmissing(df,"fixed Indiana")

# get a new dataframe with only values for Louisiana
la_fix = df.loc[df['State'] == 'Louisiana']

# drop all of the columns except for divorce rate
la_fix.drop(['Marriage rate', 'Year'], axis=1, inplace=True)

# calculate the mean divorce rate for a subset of data containing only Ohio and Iowa.
mean_div = df['divorce_rate'].loc[df['State'].isin(['Ohio', 'Iowa'])].mean()

# set all of the divorce rates in indiana_fix to be the mean of both Ohio and Iowa
la_fix['divorce_rate'] = mean_div

# fill the values to original dataframe
df.fillna(la_fix, inplace=True)

# printmissing(df,"fixed Louisiana")

# use forward fill method for the rest states which are missing values
ffillfix = df.fillna(method='ffill')

# fill the values to original dataframe
df = df.fillna(ffillfix)

# printmissing(df,'sss')

# output to csv file
df.to_csv('hw5data/fixedhw5_1.csv', index=False)
