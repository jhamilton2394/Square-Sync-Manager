import createProducts as cp

######------PROGRAM FLOW FUNCTIONS------######


### Settings menu layout
def settingsMenu():
    while True:
        print('settings menu'
              '\n')
        print('a - Set API key \n'
              'b - back')
        settingOption = input('Select an option. \n')
        if settingOption == 'a':
            apiKeyInput()
        elif settingOption == 'b':
            break
        elif settingOption != ['a', 'b']:
            print('not a valid selection. \n'
                    '\n')
            
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

### Product menu layout
def productMenu():
    while True:
        choice = input('Would you like to create one, or multiple products? \n'
                    '1 - one product \n'
                    '2 - multiple products \n'
                    '3 - back \n')
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
            input('Please press enter to select file containing properly formatted inventory. \n'
                  '(See inventory formatting guidelines for more info) \n')
            cp.createAllProducts(cp.openFile(), str(pageSelect()))
        elif choice == '3':
            break