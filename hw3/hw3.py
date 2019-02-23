#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

@author: audreytinkey

"""

import pandas as pd


# Setting variables for all 7 file names
a = 'h08.xls'
b = 'Health Insurance Coverage Type by Family Income and Age 2008-2017.csv'
c = 'state-divorce-rates-90-95-99-17.xlsx'
d = 'state-marriage-rates-90-95-99-17.xlsx'
e = 'tab-a-1.xls'
g = 'Unemployment rate by state 2000-2017.csv'
h = 'CrimeTrendsInOneVar.csv'

# h2 is the file name for h after the merger function
h2 = 'merged_CrimeTrendsInOneVar.csv'


# Reads CSV files and converts to DataFrame.
def csv(f, sr, sf, na, ic, head):
    df = pd.read_csv('data/{0}'.format(f),
                     skiprows=sr,
                     skipfooter=sf,
                     header=head,
                     na_values=na,
                     index_col=ic,
                     )
    return df


# Reads Excel files and converts to DataFrame.
def excel(f, sr, sf, na, ic, head):
    df = pd.read_excel('data/{0}'.format(f),
                       skiprows=sr,
                       header=head,
                       na_values=na,
                       skipfooter=sf,
                       index_col=ic
                       )
    return df


# Merges two CrimeTrendsInOneVar files into one DataFrame
def merger(f, sr):
    y = pd.read_csv('data/{0}'.format(f), skiprows=sr)
    z = pd.read_csv('data/{0} (1).csv'.format(f.split('.')[0]),
                    skiprows=sr, skipfooter=2, engine='python')

    # Since original files are wonky, these two statements insert a column in
    # each DataFrame that will later be necessary for differentiating the totals
    y.insert(loc=0, column='Crime Type', value='Violent')
    z.insert(loc=0, column='Crime Type', value='Property')

    # Appends both DataFrames without doing any sorting
    merged = y.append(z, sort=False)

    # Writes appended DataFrames out to new CSV file
    merged.to_csv('data/merged_{0}'.format(f), index=False)

    # Returns new file name of merged files
    return 'merged_{0}'.format(f)


# Defines variables for the read_excel and read_csv functions, calls each
# function to read the desired file, respectively. Renames columns based on
# file name, and writes final file to system.
def cleaner(f, filenames):

    # Experimental feature, allows user to clean their own file.
    if f not in filenames:
        sr = input('How many lines need to be skipped in the header? ')
        sf = input('How many lines need to be skipped in the footer? ')
        na = input('How are null values represented in this dataset? ')
        ic = [int(x) for x in input('Enter which column(s) will be used for'
                                    ' the index (separate with only spaces, '
                                    'NOT commas): ').split()]
        head = [int(x) for x in input('Enter which column(s) will be used for'
                                      ' the header (separate with only spaces, '
                                      'NOT commas): ').split()]

    # skip_rows (sr), header (head), skip_footer (sf), index_columns (ic),
    # and na_values (na) all set by this conditional statement based on the
    # file name that the user chose.
    elif f == a:
        sr = 3
        head = [0, 1, 2]
        sf = 1
        ic = 0
        na = 'null'

    elif f == b or f == g:
        sr = 6
        na = 'N/A'
        ic = 0
        head = 0
        sf = 0

    elif f == c:
        sr = 5
        na = '---'
        sf = 7
        ic = 0
        head = 0

    elif f == d:
        sr = 5
        na = '---'
        sf = 8
        ic = 0
        head = 0

    elif f == e:
        sr = 4
        na = '(NA)'
        ic = 0
        head = [0, 1, 2]
        sf = 12

    elif f == h:
        sr = 4
        head = 0
        sf = 0
        ic = [0, 1]
        na = 'null'
        f = merger(f, sr)
        sr = 0

    # Conditional statement sends given file to be read depending on the suffix.
    # Returns DataFrame
    if '.csv' in f:
        data = csv(f, sr, sf, na, ic, head)
    elif '.xls' in f:
        data = excel(f, sr, sf, na, ic, head)
    else:
        print('Data in unsupported format. Please convert file to .csv or '
              '.xls/.xlsx before proceeding')
        exit()

    # Drops null values based on previously defined null marking.
    data.dropna(how='all', inplace=True)

    # Counts number of rows in DataFrame in case file is too big for .xls.
    count_row = data.shape[0]

    # Skips files b and g since they do not need to be stacked.
    if f != b and f != g:
        data = data.stack(head)

    # Resets DataFrame index.
    data = data.reset_index()

    # The following conditional statement changes column headers based on
    # file name.
    if f == a:
        data.rename(columns={data.columns[0]: 'State',
                             data.columns[1]: 'Currency',
                             data.columns[2]: 'Year',
                             data.columns[3]: 'Median Income/Standard Error',
                             data.columns[4]: 'USD$'},
                    inplace=True)

        # Removes junk from year names.
        for i, row in data.iterrows():
            data.at[i, 'Year'] = str(data.at[i, 'Year']).split('(')[0]

    # Drops unnecessary first column of file b and g
    elif f == b or f == g:
        data.drop(data.columns[0], axis=1, inplace=True)

    elif f == c:
        data.rename(columns={data.columns[0]: 'State',
                             data.columns[1]: 'Year',
                             data.columns[2]: 'Divorces per 1000'},
                    inplace=True)

    elif f == d:
        data.rename(columns={data.columns[0]: 'State',
                             data.columns[1]: 'Year',
                             data.columns[2]: 'Marriages per 1000'},
                    inplace=True)

    elif f == e:
        data.rename(columns={data.columns[0]: 'Years',
                             data.columns[1]: 'Type of residence in the United '
                                              'States',
                             data.columns[2]: 'Different or Same County',
                             data.columns[3]: 'Different or Same State',
                             data.columns[4]: 'Movers from Abroad'},
                    inplace=True)

        # Removes all "Unnamed" and "null" values in DataFrame
        for i, row in data.iterrows():
            if str(data.at[i, 'Different or Same County']).startswith('Unnamed'):
                data.at[i, 'Different or Same County'] = ' '
            if str(data.at[i, 'Different or Same State']).startswith('Unnamed'):
                data.at[i, 'Different or Same State'] = ' '
            if str(data.at[i, 'Movers from Abroad']) == 'null':
                data.at[i, 'Movers from Abroad'] = ' '

    elif f == h2:
        data.rename(columns={data.columns[2]: 'State',
                             data.columns[3]: 'Estimated Total'},
                    inplace=True)

        # Changes order of columns so that Year and State are first.
        data = data[['Year', 'State', 'Crime Type', 'Estimated Total']]

    # Decides whether output file can be .xls or if it must be written as .csv.
    if count_row < 65536:
        data.to_excel(excel_writer='data/cleaned/cleaned_{0}.xls'.format(f.split('.')[0]),
                      sheet_name='cleaned',
                      na_rep='null',
                      index=False)
        print('Cleaned file successfully saved in .xls format.')

    else:
        data.to_csv(path_or_buf='data/cleaned/cleaned_{0}.csv'.format(f.split('.')[0]),
                    na_rep='null',
                    index=False)
        print('Notice: your file was too large to be converted to Excel format,'
              ' and has successfully been saved as .csv')


# User is able to type the name of which file they want to clean, and specify
# whether they would like to clean another once it is done.
def main():

    while True:
        filenames = [a, b, c, d, e, g, h]

        f = input('Please enter the name of the file that you want to use: ')

        cleaner(f, filenames)

        while True:
            answer = input('Would you like to clean another file? (y/n): ')
            if answer in ('y', 'n', 'Y', 'N'):
                break

            else:
                answer = input('Invalid input. Would you like to run this '
                               'program again? (y/n): ')
                if answer in ('y', 'n', 'Y', 'N'):
                    break
                else:
                    exit()

        # If user determines that they would like to clean another file, program
        # will loop back, otherwise break.
        if answer == 'y' or answer == 'Y':
            continue

        else:
            print('Thank you, goodbye.')
            break


# Sort of a boilerplate for this script, shows all names of files that are
# available to be analyzed. Only runs the first time the script is run.
print('This program supports any of the following file names:\n', a, '\n',
      b, '\n', c, '\n', d, '\n', e, '\n', g, '\n', h, '\n Custom files may'
      ' be supported by this program.')
main()
