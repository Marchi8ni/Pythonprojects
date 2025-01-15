import pandas
import openpyxl

pd = pandas.read_excel('europe.xlsx')
print(pd)

convert = pd.to_csv('europe.csv')
