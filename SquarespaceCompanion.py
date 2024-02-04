### Squarespace Companion v0.0.3.1 released January 24th 2024

###This is the main file. It houses the main structure of the program. The options menu items will call their respective
#  functions from the menu file. The menu file functions will call the meat and potatoes functions from the CreateProducts file.
from time import sleep
import menu as m



######------MAIN STRUCTURE------######


### Command line menu loop
print('Welcome to Squarespace Companion!\n'
      '\n'
      'If you have not already, please configure your settings\n'
      'under the settings option in the main menu. \n')
sleep(1)
while True:
    print('\n ---Main menu--- \n')
    print('1 - Create Products \n'
          '2 - Settings \n'
          '3 - Info \n'
          'x - Exit \n')
    selection = input('\n Select an option. \n'
                      '\n')
    if selection == '1':
        m.productMenu()
        print('\n')
    elif selection == '2':
        m.settingsMenu()
    elif selection == '3':
        m.infoMenu()
    elif selection == 'x':
        break
    elif selection != ['1', '2', '3', 'x']:
        print('not a valid selection'
              '\n')