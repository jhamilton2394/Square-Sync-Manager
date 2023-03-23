###PROGRAM FLOW FUNCTIONS



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
            

### API key input
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