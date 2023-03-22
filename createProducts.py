import requests
from json import dumps
from pandas import ExcelFile
import keys as k



#inventory='C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx'

### Defining our function to import the excel file containing inventory to be loaded to squarespace.
#   the parameter "file" must be a complete file path ending in a document of type .xlsx
def importInventory(file):
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    return print(df)



### Function manually creates a single new product. Function works.
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
    prodHeaders = {'Authorization': 'Bearer ' + k.apiKey,
               'User-Agent': 'APIAPP1.0',
               'Content-Type': 'application/json'}
    r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return



### Function takes a spreadsheet with the below titles, and uploads all items to site.
# Uses the createProduct function in a loop.
# C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx is the path to the test file
# parameter needs to be a complete file path like example above, must terminate in .xlsx file.
def createAllProducts(file):
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    for i in range(len(df)):
        sku = str((df.loc[i].at["SKU"]))
        name = (df.loc[i].at["Name"])
        itemDesc = (df.loc[i].at["Item Description"])
        price = str((df.loc[i].at["Price"]))
        pageID = '6404283498e5bf333e47441a'
        createProduct(storePageID=pageID,
                        productName=name,
                       productDescription=itemDesc,
                      variantSku=sku,
                     productPrice=price)



### Defining our function getInventory, which will retreive one page of inventory
def getInventory():
    url = 'https://api.squarespace.com/1.0/commerce/inventory'
    # Need to provide curson for pagination
    headers = {'Authorization': 'Bearer ' + k.apiKey,
               'User-Agent': 'APIAPP1.0'}
    r = requests.get(url,headers=headers)
    prettyData = json.dumps(r.json(), indent=3)
    print(r, prettyData)



### Defining out function getProducts, which retreives one page of products
def getProducts():
    prodURL = 'https://api.squarespace.com/1.0/commerce/products'
    prodHeaders = {'Authorization': 'Bearer ' + k.apiKey,
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

#getStorePagesHeaders = {'Authorization': 'Bearer ' + k.apiKey,
#                        'User-Agent': 'APIAPP1.0'}

#getStorePages = requests.get(getStorePagesURL, headers=getStorePagesHeaders)

#print(getStorePages, getStorePages.json())

#6404283498e5bf333e47441a



### Updates a product name only, can be changed if needed.
def ProductUpdate(prodID, name):
    prodUpURL = 'https://api.squarespace.com/1.0/commerce/products/'
    prodUpHeaders = {'Authorization': 'Bearer ' + k.apiKey,
                     'User-Agent': 'APIAPP1.0',
                     'Content-Type': 'application/json'}
    nameChange = {'name': name}
    jsonNameChange = json.dumps(nameChange)
    r = requests.post(prodUpURL + prodID, headers = prodUpHeaders, data = jsonNameChange)
    json_var = r.json
    return print(r, json_var)
