import createProducts as cp
import urllib.request
from time import sleep





######------MAIN PROGRAM FLOW FUNCTIONS------######


### Settings menu layout
def settingsMenu():
    while True:
        print('settings menu'
              '\n')
        print('a - Set API key \n'
              'c - Column header configuration \n'
              'b - back \n')
        settingOption = input('Select an option. \n')
        if settingOption == 'a':
            apiKeyInput()
        elif settingOption == 'c':
            settingOption2 = input('1 - Check configuration \n'
                                   '2 - Set configuration \n')
            if settingOption2 == '1':
                column_header_configuration_read()
            elif settingOption2 == '2':
                column_header_configuration_write()
        elif settingOption == 'b':
            break
        elif settingOption != ['a', 'b']:
            print('not a valid selection. \n'
                    '\n')
            
### Info menu layout
def infoMenu():
    while True:
        choice = input('Info menu \n'
                       '1 - Inventory spreadsheet configuration \n'
                       'b - back \n')
        if choice == '1':
            info_inventory_spreadsheet_configuration()
        elif choice == 'b':
            break

### Product menu layout
def productMenu():
    while True:
        while True:
            if connect():
                choice = input('Would you like to create one, or multiple products? \n'
                            '1 - one product \n'
                            '2 - multiple products \n'
                            '3 - back \n'
                            '\n')
                if choice == '1':
                    name = input('enter the product name \n')
                    description = input('enter the product description \n')
                    sku = input('enter the product SKU \n')
                    price = input('enter the product price \n')
                    quantity = input('enter the product quantity \n')
                    choice2 = input('Are you sure you want to create a product with the info you entered? \n'
                                    'y - yes \n'
                                    'n - no \n')
                    if choice2 == 'y':
                        cp.createProduct(str(pageSelect()), name, description, sku, price, quantity)
                        break
                elif choice == '2':
                    input('Please press enter to select file containing properly formatted inventory, \n'
                        'then navigate back to this window.'
                        '(See inventory formatting guidelines for more info) \n')
                    cp.createAllProducts(cp.openFile(), str(pageSelect()))
                elif choice == '3':
                    break
            else:
                print('You are not connected to the internet. \n'
                      'Please connect and try again. \n')
                sleep(3)
                break
        break





######------SUB MENU FUNCTIONS------######


### API key input. Saves api key to file called keyfile.txt. Used in settings menu.
def apiKeyInput():
    while True:
        apiKey = input("Please enter your API key, or press 'b' to go back. \n")
        if apiKey == 'b':
            break
        while True:
            response = input('You typed ' + apiKey + ', is that correct? \n'
                        'y - yes \n'
                        'n - no \n')
            if response == 'y':
                file1 = open('keyfile.txt', 'w')
                file1.write(apiKey)
                print('Your API key has been saved. \n')
                break
            elif response == 'n':
                break
            elif response != ['y', 'n']:
                print('That is not a valid response. \n')
                continue

### Uses pagesList to show user available pages then has them choose the one they want.
#   returns the selected page id
def pageSelect():
    print('These are the available pages for product import: \n')
    cp.pagesList()
    print('\n')
    while True:
        selectedPage = input('enter the page id you would like to import products to (copy and paste it). \n'
                            'or you can press "b" to go back.')
        if selectedPage == 'b':
            break
        resp = input('you chose ' + selectedPage + ', is that correct? \n'
                    'y - yes \n'
                    'n - no \n')
        if resp == 'y':
            break
        elif resp == 'n':
            continue
        elif resp != ['y', 'n']:
            continue
    return selectedPage


### checks internet connection to prevent crash when user isn't connected to the internet.
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
    
#print('connected' if connect() else 'no internet')

### Displays instructions on how to setup Squarespace companion to interface with their spreadsheet
def info_inventory_spreadsheet_configuration():
    while True:
        choice = input('In order for Squarespace Companion to interface with your inventory spreadsheet \n'
                       'it needs to know the column headers that are used. For example; if your items are \n'
                       'listed in rows, you probably have data such as "name", "description", and "price", \n'
                       'set as the column headers. \n'
                       '\n'
                       'The column headers that are required to be configured are: \n'
                       'name \n'
                       'SKU \n'
                       'item description \n'
                       'price \n'
                       'quantity \n'
                       '\n'
                       'If your inventory spreadsheet does not have columns with this info then you must \n'
                       'create them. This is the minimum info needed to create new products. \n'
                       'How to set the configuration: \n'
                       'Navigate to the settings menu and select "column header configuration" \n'
                       'You will be prompted to enter the column header names that correspond \n'
                       'to the above headers EXACTLY as they appear on your spreadsheet. \n'
                       'It is very important that your input matches exactly, it is case sensitive. \n'
                       'Once they are saved you don\'t need to set them again unless you change \n'
                       'them on your spreadsheet. \n'
                       '\n'
                       'b - back \n')
        if choice == 'b':
            break

### Configures the column headers for product creation. Needs to configure name, sku, item description, price, and qty
def column_header_configuration_write():
    name_var = input('Enter the column heading for the "name" column as it reads on your inventory excel sheet. \n')
    file = open('namefile.txt', 'w')
    file.write(name_var)
    sku_var = input('Enter the column heading for the "SKU" column as it reads on your inventory excel sheet. \n')
    file1 = open('skufile.txt', 'w')
    file1.write(sku_var)
    item_desc_var = input('Enter the column heading for the "item description" column as it reads on your inventory excel sheet. \n')
    file2 = open('item_desc_file.txt', 'w')
    file2.write(item_desc_var)
    price_var = input('Enter the column heading for the "price" column as it reads on your inventory excel sheet. \n')
    file3 = open('pricefile.txt', 'w')
    file3.write(price_var)
    qty_var = input('Enter the column heading for the "quantity" column as it reads on your inventory excel sheet. \n')
    file4 = open('qtyfile.txt', 'w')
    file4.write(qty_var)
    print('saved')

### reads and prints column header configurations
def column_header_configuration_read():
    name1 = open('namefile.txt', 'r')
    nameHeader = (name1.read())
    print('name header set to ', nameHeader, '\n')
    sku = open('skufile.txt', 'r')
    skuHeader = (sku.read())
    print('SKU header set to ', skuHeader, '\n')
    item_desc = open('item_desc_file.txt', 'r')
    item_desc_header = (item_desc.read())
    print('Item description header set to ', item_desc_header, '\n')
    price = open('pricefile.txt', 'r')
    priceHeader = (price.read())
    print('Price header set to ', priceHeader, '\n')
    qty = open('qtyfile.txt', 'r')
    qtyHeader = (qty.read())
    print('Quantity header set to ', qtyHeader, '\n')