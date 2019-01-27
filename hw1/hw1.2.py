import pandas as pd                                                     # import pandas for data reading and manipulating libraries

divorce = pd.read_excel('data/state-divorce-rates-90-95-99-17.xlsx',    # read from this file name
                        skiprows=5,                                     # skip first 5 rows of metadata/description
                        na_values='---',                                # defines null values in file
                        skipfooter=7,                                   # skip last 7 rows of metadata/description
                        )

divorce.rename(columns={'Unnamed: 0': 'State'}, inplace=True)           # renames cell A1 to "State"
divorce.dropna(how='all', inplace=True)                                 # replaces all values that have been designated as null
divorce.to_excel(excel_writer='data/divorce_clean.xls',                 # output changes to new excel file
                 sheet_name='divorce rate',                             # sheet name
                 na_rep='null')                                         # defines how we want to display null values
