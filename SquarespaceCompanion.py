###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts as cp
import requests
import json

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

#for i in range(len(df)):
#    sku = (df.loc[i].at["SKU"])
#    name = (df.loc[i].at["Name"])
#    itemDesc = (df.loc[i].at["Item Description"])
#    price = (df.loc[i].at["Price"])
#    pageID = '6404283498e5bf333e47441a'
#    #cp.createProduct(storePageID=pageID,
#    #                productName=name,
#    #               productDescription=itemDesc,
#    #              variantSku=sku,
#    #             productPrice=price)
#    print(sku, name, itemDesc, price, pageID)


#the function returns a "not authorized error" skip below to try it outside of function
#cp.createProduct('6404282c841d1330686393f7', 'bananas', '<p> a bundle of bananas </p>', '2342', '400')



###get pagws
#getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'

#getStorePagesHeaders = {'Authorization': 'Bearer bb931555-22ae-48f9-8ab5-9ff5b3744eb6',
#                        'User-Agent': 'APIAPP1.0'}

#getStorePages = requests.get(getStorePagesURL, headers=getStorePagesHeaders)

#print(getStorePages, getStorePages.json())

##6404282c841d1330686393f7



### attempting product creation without function
###This one worked, the header was missing the word "Bearer". The correction has been made to the function.
#dataOutbox = {'type': 'PHYSICAL',
#              'storePageId': '6404282c841d1330686393f7',
#               'name': 'bananas',
#               'description': '<p> a bundle of bananas </p>',
#               'isVisible': 'true',
#               'variants': [{'sku': '23456',
#                            'pricing': {'basePrice': {'currency': 'USD',
#                                                      'value': '85'
#                                                      }
#                                        }
#                             }
#                            ]
#                }

#jsonDataOutbox = json.dumps(dataOutbox)
#prodURL = 'https://api.squarespace.com/1.0/commerce/products'
#prodHeaders = {'Authorization': 'Bearer 960417a8-80f4-41e5-aa64-d352c9b08e0a', 'User-Agent': 'APIAPP1.0', 'Content-Type': 'application/json'}
#r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
#json_data = r.json()
#pretty_json_data = json.dumps(json_data, indent=3)
#print(r)
#print(pretty_json_data)