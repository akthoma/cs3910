import pandas as pd

print('This program supports any of the following file names:\nh08b.xls\n'
      'Health Insurance Coverage Type by Family Income and Age 2008-2017.csv\n'
      'state-divorce-rates-90-95-99-17.xlsx\nstate-marriage-rates-90-95-99-17.xlsx\n'
      'tab-a-1.xls\nUnemployment rate by state 2000-2017.csv\nCustom files may be supported'
      ' by this program.')
filenames = ['h08b.xls', 'Health Insurance Coverage Type by Family Income and Age 2008-2017.csv',
             'state-divorce-rates-90-95-99-17.xlsx', 'state-marriage-rates-90-95-99-17.xlsx',
             'tab-a-1.xls', 'Unemployment rate by state 2000-2017.csv']

f = input('Please enter the name of the file that you want to use: ')

if f not in filenames:
    sr = input('How many lines need to be skipped in the header? ')
    sf = input('How many lines need to be skipped in the footer? ')
    na = input('How are null values represented in this dataset? ')
    ic = input('Enter which column(s) will be used for the index: ')
    h = input('Enter which column(s) will be used for the header: ')
elif f == 'state-divorce-rates-90-95-99-17.xlsx':
            sr = 5
            na = '---'
            sf = 7
            ic = 0
            h = 0
elif f == 'state-marriage-rates-90-95-99-17.xlsx':
            sr = 5
            na = '---'
            sf = 8
            ic = 0
            h = 0
elif f == 'Unemployment rate by state 2000-2017.csv':
            sr = 6
            na = 'N/A'
            ic = 0
            h = 0
            sf = 0
elif f == 'tab-a-1.xls':
            sr = 4
            na = '(NA)'
            ic = 1
            h = 0
            sf = 0
elif f == 'h08b.xls':
            sr = 4
            h = [0, 1]
            sf = 1
            ic = 0
            na = 'null'
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


def csv(f, sr, sf, na, ic, h):
    d = pd.read_csv('data/{0}'.format(f),
                    skiprows=sr,
                    header=h,
                    na_values=na,
                    skipfooter=sf,
                    index_col=ic
                    )
    return d


def excel(f, sr, sf, na, ic, h):
    d = pd.read_excel('data/{0}'.format(f),
                      skiprows=sr,
                      header=h,
                      na_values=na,
                      skipfooter=sf,
                      index_col=ic
                      )
    return d


if '.csv' in f:
    data = csv(f, sr, sf, na, ic, h)
elif '.xls' in f:
    data = excel(f, sr, sf, na, ic, h)


