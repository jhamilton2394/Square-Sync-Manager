import requests
import json
from pandas import ExcelFile
from tkinter import Tk
from tkinter.filedialog import askopenfilename


class ProductBatch:
    def __init__(self, user):
        
        self.api_key = user.api_key
        self.nameHeader = user.product_name
        self.skuHeader = user.sku
        self.item_desc_header = user.item_desc
        self.priceHeader = user.price
        self.qtyHeader = user.qty
        self.delHeader = user.deleted
        self.filePath = user.file_name
        self.pageID = '65dd50b1aa45113b391e6b50'

    def createAllProducts(self):
        #opening column header files for input into loop
        # name1 = open('namefile.txt', 'r')
        # nameHeader = (name1.read())
        # sku1 = open('skufile.txt', 'r')
        # skuHeader = (sku1.read())
        # item_desc1 = open('item_desc_file.txt', 'r')
        # item_desc_header = (item_desc1.read())
        # price1 = open('pricefile.txt', 'r')
        # priceHeader = (price1.read())
        # qty1 = open('qtyfile.txt', 'r')
        # qtyHeader = (qty1.read())
        # del1 = open('delfile.txt', 'r')
        # delHeader = (del1.read())
        #open excel doc
        xls = ExcelFile(self.filePath)
        df = xls.parse(xls.sheet_names[0])
        product_list = self.site_master_prod_list()
        #loop thru doc & create products using column header files.
        for i in range(len(df)):
            sku = str((df.loc[i].at[self.skuHeader]))
            name = (df.loc[i].at[self.nameHeader])
            itemDesc = (df.loc[i].at[self.item_desc_header])
            price = str((df.loc[i].at[self.priceHeader]))
            quant = str((df.loc[i].at[self.qtyHeader]))
            del2 = (df.loc[i].at[self.delHeader])
            pageID = self.pageID
            if name in product_list:
                print(name, 'already on site, skipping...\n')
            elif del2 == 'x':
                print(name, 'previously deleted from site by user, skipping...')
            else:
                createProduct(storePageID=pageID,
                                productName=name,
                            productDescription=itemDesc,
                            variantSku=sku,
                            productPrice=price,
                            quantity=quant)
    
    def site_master_prod_list(self):
        #Initial product query
        actual_prod_list = []
        ###Commenting out 2 lines below, which just opens the data file. The file was used for testing purposes.
        # open_product_data = open('product_file', 'r')
        # raw_data = open_product_data.read()
        raw_data = self.getProducts()
        prod_main_dict = json.loads(raw_data)
        prod_list = prod_main_dict['products']
        pagination = prod_main_dict['pagination']
        cursor = pagination['nextPageCursor']
        for i in prod_list:
            actual_prod_list.append(i['name'])
        ###Loops through all pages if they exist.
        while pagination['hasNextPage'] == True:
            raw_data = self.getProducts(cursor)
            prod_main_dict = json.loads(raw_data)
            prod_list = prod_main_dict['products']
            pagination = prod_main_dict['pagination']
            cursor = pagination['nextPageCursor']
            for i in prod_list:
                actual_prod_list.append(i['name'])
        return actual_prod_list
        
    ### Defining out function getProducts, which retreives one page of products. Optionally takes a cursor.
    def getProducts(self, cursor=''):
        prodURL = 'https://api.squarespace.com/1.0/commerce/products?cursor=' + cursor
        prodHeaders = {'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': 'APIAPP1.0'}
        r = requests.get(prodURL, headers=prodHeaders)
        json_data = r.json()
        pretty_json_data = json.dumps(json_data, indent=3)
        return pretty_json_data



    def getPagesList(x):
        getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
        api_key = '72a30b97-cac8-48e4-b8d7-31bcd6313c29'
        #replaced retreiveAPIKey() with api_key
        getStorePagesHeaders = {'Authorization': 'Bearer ' + api_key,
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
        api_key = '72a30b97-cac8-48e4-b8d7-31bcd6313c29'
        getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
        # replaced retreiveApiKey() function with api_key for testing
        getStorePagesHeaders = {'Authorization': 'Bearer ' + api_key,
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


### File originally created only for the create products functions, but it ended up growing.
# It is now too inconvenient to try to rename it, so it is going to stay "create products"
# It should honestly just be named "functions" or something.

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
# newFile = productFile.write(prod_list_test.getProducts())

### Calls 'get products' to retreive product data, converts it to a dictionary, then extrapolates each name from each product
#   and puts it in a list of names. If there are multiple pages of products, it will loop through all
#   pages and add those products to the list as well





######------PAGES FUNCTIONS------######


### gets a list of pages and their id's, as well as some other random info that is included.
#   returns name and id of specified page number only. This function is only intended to be
#   called by the function 'pagesList'.
def getPagesList(x):
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    api_key = '72a30b97-cac8-48e4-b8d7-31bcd6313c29'
    #replaced retreiveAPIKey() with api_key
    getStorePagesHeaders = {'Authorization': 'Bearer ' + api_key,
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
    api_key = '72a30b97-cac8-48e4-b8d7-31bcd6313c29'
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    # replaced retreiveApiKey() function with api_key for testing
    getStorePagesHeaders = {'Authorization': 'Bearer ' + api_key,
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