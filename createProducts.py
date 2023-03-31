### File originally created only for the create products functions, but it ended up growing.
# It is now too inconvenient to try to rename it, so it is going to stay "create products"
# It should honestly just be named "functions" or something.

import requests
import json
from pandas import ExcelFile
from tkinter import Tk
from tkinter.filedialog import askopenfilename





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

    ### function grabs the api key from the keyfile.txt file for use in requests
def retreiveApiKey():
    file = open('keyfile.txt', 'r')
    retreivedKey = file.read()
    return retreivedKey





######------PRODUCT CREATION FUNCTIONS------######


### Function takes a spreadsheet with the below titles, and uploads all items to site. Also takes page id.
# Uses the createProduct function in a loop.
# parameter for file needs to be a complete file path like example above, must terminate in .xlsx file.
# to get the id parameter "pagesList" should be called and the applicable id pasted in.
# HERE is the format for loading the column headers:
# name1 = open('namefile.txt', 'r')
# nameHeader = (name1.read())
# Stick all column header files at top of create allproducts funct for use in the loop.
def createAllProducts(file, id):
    #opening column header files for input into loop
    name1 = open('namefile.txt', 'r')
    nameHeader = (name1.read())
    sku1 = open('skufile.txt', 'r')
    skuHeader = (sku1.read())
    item_desc1 = open('item_desc_file.txt', 'r')
    item_desc_header = (item_desc1.read())
    price1 = open('pricefile.txt', 'r')
    priceHeader = (price1.read())
    qty1 = open('qtyfile.txt', 'r')
    qtyHeader = (qty1.read())
    #open excel doc
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    #loop thru doc & create products using column header files.
    for i in range(len(df)):
        sku = str((df.loc[i].at[skuHeader]))
        name = (df.loc[i].at[nameHeader])
        itemDesc = (df.loc[i].at[item_desc_header])
        price = str((df.loc[i].at[priceHeader]))
        quant = str((df.loc[i].at[qtyHeader]))
        pageID = id
        createProduct(storePageID=pageID,
                        productName=name,
                       productDescription=itemDesc,
                      variantSku=sku,
                     productPrice=price,
                     quantity=quant)
        
### Function manually creates a single new product.
def createProduct(storePageID, productName, productDescription, variantSku, productPrice, quantity):
    dataOutbox = {'type': 'PHYSICAL',
              'storePageId': storePageID,
               'name': productName,
               'description': productDescription,
               'isVisible': 'true',
               'variants': [{'sku': variantSku,
                            'pricing': {'basePrice': {'currency': 'USD',
                                                      'value': productPrice
                                                      }
                                         },
                            'stock': {'quantity': quantity}}
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
    return pretty_json_data

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

### used the below code to write a products request to a file
# productFile = open('product_file', 'w')
# newFile = productFile.write(getProducts())


def prod_list_test():
### opens above mentioned file, converts it to a dictionary,
    open_product_data = open('product_file', 'r')
    raw_data = open_product_data.read()
    prod_main_dict = json.loads(raw_data)
    prod_list = prod_main_dict['products']
    for i in prod_list:
        for key in i.keys():
            print(key)

prod_list_test()
        # first_prod_name = first_prod_in_list['name']
        # print(first_prod_name)


# for i in first_key:
#     first_element = first_key[i]
#     first_name = first_element['name']
#     print(first_name)
# first_element = first_key[0]
# first_prod_name = first_element['name']
# print(first_prod_name)



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
    # return numOfPages
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