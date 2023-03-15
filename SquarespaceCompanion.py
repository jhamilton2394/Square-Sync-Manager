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
    sku = (df.loc[i].at["SKU"])
    name = (df.loc[i].at["Name"])
    itemDesc = (df.loc[i].at["Item Description"])
    price = (df.loc[i].at["Price"])
    pageID = '6404283498e5bf333e47441a'
    #cp.createProduct(storePageID=pageID,
    #                productName=name,
    #               productDescription=itemDesc,
    #              variantSku=sku,
    #             productPrice=price)
    print(sku, name, itemDesc, price, pageID)