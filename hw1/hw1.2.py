import pandas as pd

divorce = pd.read_excel('data/state-divorce-rates-90-95-99-17.xlsx',    # read from this file name
                        skiprows=5,                                     # skip first 5 rows of metadata/description
                        na_values='---',                                # defines null values in file
                        skipfooter=7,                                   # skip last 7 rows of metadata/description
                        index_col=0)                                    # defines column A as the index

divorce.dropna(how='all', inplace=True)                                 # replaces all values that have been marked null
divorce = divorce.stack()                                               # stacks state and year indexes
divorce.index.names = ['State', 'Year']                                 # renames indexes appropriately
divorce.name = "Divorces Per 1000"                                      # renames series header
divorce.to_excel(excel_writer='data/divorce_clean.xls',                 # output changes to new excel file
                 sheet_name='divorce rate',                             # define sheet name
                 na_rep='null')                                         # defines how we want to display null values
