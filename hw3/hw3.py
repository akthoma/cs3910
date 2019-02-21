import pandas as pd


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


def merger(f):
    a = pd.read_csv('data/{0}'.format(f))
    b = pd.read_csv('data/{0} (1)'.format(f))
    b = b.dropna(axis=1)
    merged = a.merge(b, on='title')
    merged.to_csv('data/{0}.csv'.format(f), index=False)


a = 'h08b.xls'
b = 'Health Insurance Coverage Type by Family Income and Age 2008-2017.csv'
c = 'state-divorce-rates-90-95-99-17.xlsx'
d = 'state-marriage-rates-90-95-99-17.xlsx'
e = 'tab-a-1.xls'
g = 'Unemployment rate by state 2000-2017.csv'
h = 'CrimeTrendsInOneVar.csv'


print('This program supports any of the following file names:\n',a, '\n',
      b, '\n', c, '\n', d, '\n', e, '\n', g, '\n', h, '\n'
      'Custom files may be supported by this program.')

filenames = [a, b, c, d, e, g, h]

f = input('Please enter the name of the file that you want to use: ')

if f not in filenames:
    sr = input('How many lines need to be skipped in the header? ')
    sf = input('How many lines need to be skipped in the footer? ')
    na = input('How are null values represented in this dataset? ')
    ic = [int(x) for x in input('Enter which column(s) will be used for the index'
                                ' (separate with only spaces, NOT commas): ').split()]
    h = [int(x) for x in input('Enter which column(s) will be used for the header'
                               ' (separate with only spaces, NOT commas): ').split()]
elif f == a:
    sr = 4
    h = [0, 1]
    sf = 1
    ic = 0
    na = 'null'
elif f == b or f == g:
    sr = 6
    na = 'N/A'
    ic = 0
    h = 0
    sf = 0
elif f == c:
    sr = 5
    na = '---'
    sf = 7
    ic = 0
    h = 0
elif f == d:
    sr = 5
    na = '---'
    sf = 8
    ic = 0
    h = 0
elif f == e:
    sr = 4
    na = '(NA)'
    ic = 0
    h = [0, 1, 2]
    sf = 12
elif f == h:
    merger(f)
    sr = 4
    h = 0
    sf = 1
    ic = 0
    na = 'null'

if '.csv' in f:
    data = csv(f, sr, sf, na, ic, h)
elif '.xls' in f:
    data = excel(f, sr, sf, na, ic, h)
else:
    print('Data in unsupported format. Please convert file to .csv or .xls/.xlsx'
          'before proceeding')
    exit()

data.dropna(how='all', inplace=True)
count_row = data.shape[0]

if f != b and f != g:
    data = data.stack(h)

if f == a:
    data.rename(columns={'level_0': 'State',
                         data.columns[1]: 'Year',
                         'level_2': 'Income',
                         0: 'USD$'},
                inplace=True)
elif f == c:
    data.index.names = ['State', 'Year']
    data.name = 'Divorces Per 1000'
elif f == d:
    data.index.names = ['State', 'Year']
    data.name = 'Marriages Per 1000'
elif f == e:
    data.rename(columns={data.columns[0]: 'Years',
                         data.columns[1]: 'Type of residence in the United States',
                         data.columns[2]: 'Different or Same County',
                         data.columns[3]: 'Different or Same State',
                         data.columns[4]: 'total',
                         }, inplace=True)
# elif f == 'CrimeOneYearofData.csv':

data = data.reset_index()

if count_row < 65536:
    data.to_excel(excel_writer='data/cleaned/cleaned_{0}.xls'.format(f),
                  sheet_name='cleaned_{0}'.format(f),
                  na_rep='null',
                  index=False)
    print('Cleaned file successfully saved in .xls format.')
else:
    data.to_csv(path_or_buf='data/cleaned/cleaned_{0}.csv'.format(f),
                na_rep='null',
                index=False)
    print('Notice: your file was too large to be converted to Excel format, and has'
          ' successfully been saved as .csv')

