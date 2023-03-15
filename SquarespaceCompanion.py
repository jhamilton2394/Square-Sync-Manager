###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts as cp

#x  = input('would you like to run the function?')
#if x == 'yes':
#    cp.createProduct(storePageID='6404283498e5bf333e47441a',
#                     productName='Posies',
#                     productDescription='<p> some posies </p>',
#                     variantSku='8008s',
#                     productPrice='100')

from pandas import *
xls = ExcelFile('C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx')

df = xls.parse(xls.sheet_names[0])

for i in range(len(df)):
    (df.loc[i].at["SKU"])
    print(df.loc[i].at["Name"])
    print(df.loc[i].at["Item Description"])

