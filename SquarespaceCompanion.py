###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts as cp
import json
import keys as k
import pandas
import tkinter as tk
import customtkinter as ctk
import requests
import time
import menu as m


### Command line menu loop
print('Welcome to Squarespace Companion!\n'
      '\n'
      'If you have not already, please configure your settings\n'
      'under the settings option in the main menu.')
time.sleep(1)

#Start the menu loop
while True:
    print('Main menu \n')
    print('c - Create Products \n'
          's - Settings \n'
          'x - Exit \n')
    selection = input('Select an option. \n'
                      '\n')

    if selection == 'c':
        m.productMenu()
        print('\n')

    elif selection == 's':
        m.settingsMenu()

    elif selection == 'x':
        break

    elif selection != ['c', 's', 'x']:
        print('not a valid selection'
              '\n')



### Working on a version of import excel that imports .numbers files
# from numbers_parser import Document
# doc = Document('/Users/jonathan/Downloads/DRESS INVENTORY.numbers')
# sheets = doc.sheets()
# tables = sheets[0].tables()
# rows = tables[0].rows()

# newDict = dict(doc)

# print(type(newDict))