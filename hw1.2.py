import pandas as pd

divorce = pd.read_excel('data/state-divorce-rates-90-95-99-17.xlsx',
                        skiprows=5,
                        na_values='---',
                        skipfooter=7,
                        )

# divorce = divorce.set_index()
divorce.rename(columns={'Unnamed: 0': 'State'}, inplace=True )
divorce.dropna(how='all', inplace=True)
divorce.to_excel(excel_writer='data/divorce_clean.xls',
                 sheet_name='divorce rate',
                 na_rep='null',
                 index=False)
