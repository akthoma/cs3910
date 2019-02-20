import pandas as pd
from glob import *

def main():

    filenames = []
    for file in glob("*.csv" | "*.xls" | "*.xlsx"):
        filenames.append(file)

    for f in filenames:
        if f == 'state-divorce-rates-90-95-99-17.xlsx':
            sr = 5
            na = '---'
            sf = 7
            ic = 0
        elif f == 'state-marriage-rates-90-95-99-17.xlsx':
            sr = 5
            na = '---'
            sf = 8
            ic = 0
        elif f == 'Unemployment rate by state 2000-2017.csv':
            sr = 6
            na = 'N/A'
            ic = 0
        elif f == 'tab-a-1.xls':
            sr = 4
            h = [0, 1, 2]
            na = '(NA)'
            ic = 1
        elif f == 'h08b.xls':
            sr = 4
            h = [0, 1]
            sf = 1
            ic = 0
        # elif f == 'Health Insurance Coverage Type by Family Income and Age 2008-2017.csv':
        #    sr = 5
        #    na = "---"
        #    sf = 7
        #    index_col = 0
        # elif f == 'CrimeOneYearofData.csv':
        #    sr = 5
        #    na = "---"
        #    sf = 7
        #    index_col = 0
        else:
            print('Error: check your filenames. Filename mismatch in code.')

        if '.csv' in f:
            csv(f)
        elif ('xls' | 'xlsx') in f:
            excel(f)



        df.to_excel(excel_writer=('data/cleaned/', f),
                    sheet_name=f,
                    na_rep='null')

    print('All files have successfully been cleaned.')

def excel(f):
    data = pd.read_excel(f,
                        skiprows = sr,
                        header = h,
                        na_values = na,
                        skipfooter = sf,
                        index_col = ic
                        )

def csv(f):
    data = pd.read_csv(f,
                        skiprows = sr,
                        header = h,
                        na_values = na,
                        skipfooter = sf,
                        index_col = ic
                        )
