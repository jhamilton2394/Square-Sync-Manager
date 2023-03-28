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

#Start the menu loop
while True:
    print('Main menu \n')
    print('c - Create Products \n'
          's - Settings \n'
          'i - Info \n'
          'x - Exit \n')
    selection = input('Select an option. \n'
                      '\n')
    if selection == 'c':
        m.productMenu()
        print('\n')
    elif selection == 's':
        m.settingsMenu()
    elif selection == 'i':
        m.infoMenu()
    elif selection == 'x':
        break
    elif selection != ['c', 's', 'i', 'x']:
        print('not a valid selection'
              '\n')