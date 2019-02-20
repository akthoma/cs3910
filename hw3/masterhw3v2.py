import pandas as pd

f = input('Please enter the name of the file that you want to use: ')
sr = input('How many lines need to be skipped in the header? ')
sf = input('How many lines need to be skipped in the footer? ')
na = input('How are null values represented in this dataset? ')
ic = input('Enter which column(s) will be used for the index: ')
h = input('Enter which column(s) will be used for the header. Enter "d" to use default value: ')

if h == "d" | h == "D":
    h = 0


def csv(f, sr, sf, na, ic, h):
    d = pd.read_csv(('data/', f),
                    skiprows=sr,
                    header=h,
                    na_values=na,
                    skipfooter=sf,
                    index_col=ic
                    )
    return d


def excel(f, sr, sf, na, ic, h):
    d = pd.read_excel(('data/', f),
                      skiprows=sr,
                      header=h,
                      na_values=na,
                      skipfooter=sf,
                      index_col=ic
                      )
    return d


if '.csv' in f:
    data = csv(f, sr, sf, na, ic, h)
elif ('xls' | 'xlsx') in f:
    data = excel(f, sr, sf, na, ic, h)


