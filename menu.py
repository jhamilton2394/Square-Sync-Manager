import createProducts as cp
import urllib.request
from time import sleep
import os.path
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename



######------MAIN PROGRAM FLOW FUNCTIONS------######


### Settings menu layout
def settingsMenu():
    while True:
        print('\n ---settings menu---'
              '\n')
        print('1 - Set API key \n'
              '2 - Select inventory file \n'
              '3 - Column header configuration \n'
              'b - back \n')
        settingOption = input('Select an option. \n'
                              '\n')
        if settingOption == '1':
            apiKeyInput()
        elif settingOption == '2':
            inventory_file_select()
        elif settingOption == '3':
            settingOption2 = input('1 - Check configuration \n'
                                   '2 - Set configuration \n'
                                   'b - back \n')
            if settingOption2 == '1':
                column_header_configuration_read()
            elif settingOption2 == '2':
                column_header_configuration_write()
            elif settingOption2 != ['1', '2', 'b']:
                print('not a valid selection \n')
        elif settingOption == 'b':
            break
        elif settingOption != ['1', '2', '3', 'b']:
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
            #verifies there is an internet connection to prevent exception
            if connect():
                choice = input('Would you like to create one, or multiple products? \n'
                            '1 - one product \n'
                            '2 - multiple products \n'
                            'b - back \n'
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
                    if check_inventory_file('inventory_path.txt') == True:
                        inventory_file = open('inventory_path.txt', 'r')
                        opened_file = inventory_file.read()
                        cp.createAllProducts(str(opened_file), str(pageSelect()))
                    else:
                        break
                elif choice == 'b':
                    break
                elif choice != ['1', '2', 'b']:
                    print('not a valid selection \n')
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

### Configures the column headers for product creation. Needs to configure name, sku, item description, price, and qty.
#   should probably incorporate a loop to cut down redundant code.
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

### reads and prints column header configurations. Has for loop for failsafe if config file doesnt exist.
def column_header_configuration_read():
    file_list = ['namefile.txt',
                     'skufile.txt',
                     'item_desc_file.txt',
                     'pricefile.txt',
                     'qtyfile.txt'
                     ]
    for i in file_list:
        if check_file(i) == True:
            file = open(i, 'r')
            Header = (file.read())
            print(i, 'is set to', Header)

### Checks to see if a file exists. should be called before attempting to read a file to prevent crash.
def check_file(file):
    file_var = os.path.isfile(file)
    if file_var == False:
        print(file, 'does not exist. Column header is not configured. \n')
    return file_var

def check_inventory_file(file):
    file_var = os.path.isfile(file)
    if file_var == False:
        print('The inventory file has not been configured. Please go to settings to do so. \n')
    return file_var

### from the settings menu, saves path to inventory excel sheet
def inventory_file_select():
    input('Please select your inventory file. NOTE: excel is currently the only file type supported. \n'
          'Once you choose a file navigate back to this window (You will not automatically be redirected) \n'
          'Please press enter to proceed to file selection. \n')
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    while True:
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        if filename.endswith('.xlsx'):
            break
        else:
            print('You must select an excel file. Navigate back to browser and select an excel file. \n')
    file = open('inventory_path.txt', 'w')
    file.write(filename)
    print('Your file selection has been saved. You do not need to set it again unless you wish to \n'
          'use a different file in the future. \n')
    input('b - back \n')