### File originally created only for the create products functions, but it ended up growing.
# It is now too inconvenient to try to rename it, so it is going to stay "create products"
# It should honestly just be named "functions" or something.

import requests
import json
from pandas import ExcelFile
import keys as k
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from menu import retreiveApiKey


######------FILE HANDLING FUNCTIONS------###### (note: some other file handling functions are in menu.py file since they have program flow.)


### Defining our function to import the excel file containing inventory to be loaded to squarespace.
#   the parameter "file" must be a complete file path ending in a document of type .xlsx
#inventory='C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx' on acer laptop only.
def importInventory(file):
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    return print(df)

### Function creates file browser popup to select the file containing inventory
def openFile():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return str(filename)
    # Must import these modules below:
    # from tkinter import Tk
    # from tkinter.filedialog import askopenfilename


######------PRODUCT CREATION FUNCTIONS------######


### Function takes a spreadsheet with the below titles, and uploads all items to site. Also takes page id.
# Uses the createProduct function in a loop.
# parameter for file needs to be a complete file path like example above, must terminate in .xlsx file.
# to get the id parameter "pagesList" should be called and the applicable id pasted in.
def createAllProducts(file, id):
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    for i in range(len(df)):
        sku = str((df.loc[i].at["SKU"]))
        name = (df.loc[i].at["Name"])
        itemDesc = (df.loc[i].at["Item Description"])
        price = str((df.loc[i].at["Price"]))
        pageID = id
        createProduct(storePageID=pageID,
                        productName=name,
                       productDescription=itemDesc,
                      variantSku=sku,
                     productPrice=price)
        
### Function manually creates a single new product.
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
    prodHeaders = {'Authorization': 'Bearer ' + retreiveApiKey(),
               'User-Agent': 'APIAPP1.0',
               'Content-Type': 'application/json'}
    r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return

######------GET AND UPDATE FUNCTIONS------######


### Defining our function getInventory, which will retreive one page of inventory
def getInventory():
    url = 'https://api.squarespace.com/1.0/commerce/inventory'
    # Need to provide curson for pagination
    headers = {'Authorization': 'Bearer ' + retreiveApiKey(),
               'User-Agent': 'APIAPP1.0'}
    r = requests.get(url,headers=headers)
    prettyData = json.dumps(r.json(), indent=3)
    print(r, prettyData)

### Defining out function getProducts, which retreives one page of products
def getProducts():
    prodURL = 'https://api.squarespace.com/1.0/commerce/products'
    prodHeaders = {'Authorization': 'Bearer ' + retreiveApiKey(),
                   'User-Agent': 'APIAPP1.0'}
    r = requests.get(prodURL, headers=prodHeaders)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    return print(r, pretty_json_data)

### Updates a product name only, can be changed if needed.
def ProductUpdate(prodID, name):
    prodUpURL = 'https://api.squarespace.com/1.0/commerce/products/'
    prodUpHeaders = {'Authorization': 'Bearer ' + retreiveApiKey(),
                     'User-Agent': 'APIAPP1.0',
                     'Content-Type': 'application/json'}
    nameChange = {'name': name}
    jsonNameChange = json.dumps(nameChange)
    r = requests.post(prodUpURL + prodID, headers = prodUpHeaders, data = jsonNameChange)
    json_var = r.json
    return print(r, json_var)

######------PAGES FUNCTIONS------######


### gets a list of pages and their id's, as well as some other random info that is included.
#   returns name and id of specified page number only. This function is only intended to be
#   called by the function 'pagesList'.
def getPagesList(x):
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    getStorePagesHeaders = {'Authorization': 'Bearer ' + retreiveApiKey(),
                            'User-Agent': 'APIAPP1.0'}
    r = requests.get(getStorePagesURL, headers=getStorePagesHeaders)
    # data is the dictionary returned by the request.
    data = r.json()
    # storePages is the 2nd key in dictionary, its value is a list of dictionaries.
    storePages = data['storePages']
    # pageOne accesses the first element of the list, which is a dictionary of the
    # first page's info. If there are multiple store pages then this is a good
    # place to start a for loop to iterate through them.
    pageOne = storePages[x]
    # pageOne has all the info we need for now. pageID and pageName are accessing
    # the specific keys and values needed for our current use.
    pageID = pageOne['id']
    pageName = pageOne['title']
    pageInfo = {pageName: pageID}
    return pageInfo

### getNumOfPages returns the number of pages. It can be called by itself if the user
#   wants the number of pages, and is also called by pagesList to be used for the range
#   of pages to be iterated over.
def getNumOfPages():
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    getStorePagesHeaders = {'Authorization': 'Bearer ' + retreiveApiKey(),
                            'User-Agent': 'APIAPP1.0'}
    r = requests.get(getStorePagesURL, headers=getStorePagesHeaders)
    # data is the dictionary returned by the request.
    data = r.json()
    # storePages is the 2nd key in dictionary, its value is a list of dictionaries.
    storePages = data['storePages']
    numOfPages = len(storePages)
    return numOfPages

### pagesList shows a list of all pages, their id's, and their page number.
#   Calls getNumOfPages and getPagesList in order to iterate over all pages.
def pagesList():
    PagesNo = getNumOfPages()
    for i in range(0, PagesNo):
        page = getPagesList(i)
        print(str(i), str(page))

### This is 'data' from getPagesList function. It is all the data returned by the website
#   excluding any new pages that have been created since pulling this data. 
{'pagination': {'nextPageUrl': None,
                'nextPageCursor': None,
                'hasNextPage': False},
'storePages': [{'id': '641a906c3f58246e8a8fe285',
                'title': 'All products',
                'isEnabled': True,
                'urlSlug': 'all-products'}]}