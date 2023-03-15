import requests
import json
from pandas import ExcelFile



#inventory='C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx'

### Defining our function to import the excel file containing inventory to be loaded to squarespace.
#   the parameter "file" must be a complete file path ending in a document of type .xlsx
def importInventory(file):
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    return print(df)



### Defining our function to manually create a new single product
def createProduct(storePageID, productName, productDescription, variantSku, productPrice):
    dataOutbox = {'type': 'PHYSICAL',
              'storePageId': storePageID,
               'name': productName,
               'description': productDescription,
               'isVisible': 'true',
               'variants': [{'sku': variantSku,
                            'pricing': {'basePrice': {'currency': 'USD',
                                                      'value': productPrice
                                                      }
                                        }
                             }
                            ]
                }

    jsonDataOutbox = json.dumps(dataOutbox)
    prodURL = 'https://api.squarespace.com/1.0/commerce/products'
    prodHeaders = {'Authorization': 'bb931555-22ae-48f9-8ab5-9ff5b3744eb6',
               'User-Agent': 'APIAPP1.0',
               'Content-Type': 'application/json'}
    r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return



### Defining our function to pull all products from excel sheet and upload them to the website.
def createAllProducts(file, storePageID, productName, productDescription, variantSku, productPri):
    df = importInventory(file)
    #STILL DEVELOPING, NEED TO ITERATE OVER THE DF AND PUT ITEMS INTO THE POST.



### Defining our function getInventory, which will retreive one page of inventory
def getInventory():
    url = 'https://api.squarespace.com/1.0/commerce/inventory'
    # Need to provide curson for pagination
    APIkey = ''
    headers = {'Authorization': APIkey,
               'User-Agent': 'APIAPP1.0'}
    r = requests.get(url,headers=headers)
    prettyData = json.dumps(r.json(), indent=3)
    print(r, prettyData)



### Defining out function getProducts, which retreives one page of products
def getProducts():
    prodURL = 'https://api.squarespace.com/1.0/commerce/products'
    prodHeaders = {'Authorization': 'Bearer yourAPIKEY',
                   'User-Agent': 'APIAPP1.0'}
    r = requests.get(prodURL, headers=prodHeaders)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    return print(r, pretty_json_data)



### Create the loop structure that will iterate through the excel sheet
#   still in development
#from pandas import *
#xls = ExcelFile('C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx')

#df = xls.parse(xls.sheet_names[0])

#for i in range(len(df)):
#    (df.loc[i].at["SKU"])
#    print(df.loc[i].at["Name"])
#    print(df.loc[i].at["Item Description"])



### Gets store pages, need to make into a function
#getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'

#getStorePagesHeaders = {'Authorization': 'Bearer bb931555-22ae-48f9-8ab5-9ff5b3744eb6',
#                        'User-Agent': 'APIAPP1.0'}

#getStorePages = requests.get(getStorePagesURL, headers=getStorePagesHeaders)

#print(getStorePages, getStorePages.json())

#6404283498e5bf333e47441a



### Updates a product name only, can be changed if needed.
def ProductUpdate(prodID, name):
    prodUpURL = 'https://api.squarespace.com/1.0/commerce/products/'
    prodUpHeaders = {'Authorization': 'Bearer yourAPIKEY',
                     'User-Agent': 'APIAPP1.0',
                     'Content-Type': 'application/json'}
    nameChange = {'name': name}
    jsonNameChange = json.dumps(nameChange)
    r = requests.post(prodUpURL + prodID, headers = prodUpHeaders, data = jsonNameChange)
    json_var = r.json
    return print(r, json_var)
