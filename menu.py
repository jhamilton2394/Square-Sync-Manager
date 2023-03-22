###PROGRAM FLOW FUNCTIONS

def settingsMenu():
    print('settings menu'
              '\n')
    print('a - Set API key \n'
              'b - back')
    while True:
        settingOption = input('Select an option. \n')

        if settingOption == 'a':
            print('setting api key. \n')

        elif settingOption == 'b':
            break

        elif settingOption != ['a', 'b']:
            print('not a valid selection. \n'
                    '\n')