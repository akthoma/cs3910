import pandas as pd

a = 'h08.xls'
b = 'Health Insurance Coverage Type by Family Income and Age 2008-2017.csv'
c = 'state-divorce-rates-90-95-99-17.xlsx'
d = 'state-marriage-rates-90-95-99-17.xlsx'
e = 'tab-a-1.xls'
g = 'Unemployment rate by state 2000-2017.csv'
h = 'CrimeTrendsInOneVar.csv'


def csv(f, sr, sf, na, ic, head):
    df = pd.read_csv('data/{0}'.format(f),
                     skiprows=sr,
                     skipfooter=sf,
                     header=head,
                     na_values=na,
                     index_col=ic,
                     )
    return df


def excel(f, sr, sf, na, ic, head):
    df = pd.read_excel('data/{0}'.format(f),
                       skiprows=sr,
                       header=head,
                       na_values=na,
                       skipfooter=sf,
                       index_col=ic
                       )
    return df


def merger(f, sr):
    y = pd.read_csv('data/{0}'.format(f), skiprows=sr, error_bad_lines=False)
    z = pd.read_csv('data/{0} (1).csv'.format(f.split('.')[0]), skiprows=sr,
                    skipfooter=2, error_bad_lines=False, engine='python')
    merged = y.append(z, sort=True)
    merged.to_csv('data/merged_{0}'.format(f), index_label=False)
    return 'merged_{0}'.format(f)


def cleaner(f, filenames):
    if f not in filenames:
        sr = input('How many lines need to be skipped in the header? ')
        sf = input('How many lines need to be skipped in the footer? ')
        na = input('How are null values represented in this dataset? ')
        ic = [int(x) for x in input('Enter which column(s) will be used for the index'
                                    ' (separate with only spaces, NOT commas): ').split()]
        head = [int(x) for x in input('Enter which column(s) will be used for the header'
                                      ' (separate with only spaces, NOT commas): ').split()]
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
        sr = 3
        head = 0
        sf = 0
        ic = 0
        na = 'null'
        f = merger(f, sr)
        sr = 0

    if '.csv' in f:
        data = csv(f, sr, sf, na, ic, head)
    elif '.xls' in f:
        data = excel(f, sr, sf, na, ic, head)
    else:
        print('Data in unsupported format. Please convert file to .csv or .xls/.xlsx'
              ' before proceeding')
        exit()

    data.dropna(how='all', inplace=True)
    count_row = data.shape[0]

    if f != b and f != g:
        data = data.stack(head)

    if f == c:
        data.index.names = ['State', 'Year']
        data.name = 'Divorces Per 1000'
    elif f == d:
        data.index.names = ['State', 'Year']
        data.name = 'Marriages Per 1000'

    data = data.reset_index()

    if f == a:
        data.rename(columns={data.columns[0]: 'State',
                             data.columns[1]: 'Currency',
                             data.columns[2]: 'Year',
                             data.columns[3]: 'Median Income/Standard Error',
                             data.columns[4]: 'USD$'},
                    inplace=True)
        for i, row in data.iterrows():
            data.at[i, 'Year'] = str(data.at[i, 'Year']).split('(')[0]

    elif f == e:
        data.rename(columns={data.columns[0]: 'Years',
                             data.columns[1]: 'Type of residence in the United States',
                             data.columns[2]: 'Different or Same County',
                             data.columns[3]: 'Different or Same State',
                             data.columns[4]: 'total',
                             }, inplace=True)

    if count_row < 65536:
        data.to_excel(excel_writer='data/cleaned/cleaned_{0}.xls'.format(f),
                      sheet_name='cleaned',
                      na_rep='null',
                      index=False)
        print('Cleaned file successfully saved in .xls format.')
    else:
        data.to_csv(path_or_buf='data/cleaned/cleaned_{0}.csv'.format(f),
                    na_rep='null',
                    index=False)
        print('Notice: your file was too large to be converted to Excel format, and has'
              ' successfully been saved as .csv')


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
                input('Invalid input. Would you like to run this program again? (y/n): ')
                if answer in ('y', 'n', 'Y', 'N'):
                    break
                else:
                    exit()

        if answer == 'y' or answer == 'Y':
            continue
        else:
            print('Thank you, goodbye.')
            break


print('This program supports any of the following file names:\n', a, '\n',
      b, '\n', c, '\n', d, '\n', e, '\n', g, '\n', h, '\n Custom files may'
      ' be supported by this program.')
main()
