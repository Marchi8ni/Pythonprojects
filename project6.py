import pandas

pd = pandas.read_excel('input.xlsx')
pd['Total'] = pd['Price']*pd['Quantity']
pd.to_excel('output.xlsx')