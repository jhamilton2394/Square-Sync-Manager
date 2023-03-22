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


###CURRENTLY WORKING ON RETREIVING PAGE ID FOR USE IN PRODUCT CREATION
###get pages, gets page ID's
def getPages():
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    getStorePagesHeaders = {'Authorization': 'Bearer ' + k.apiKey,
                            'User-Agent': 'APIAPP1.0'}
    r = requests.get(getStorePagesURL, headers=getStorePagesHeaders)
    data = r.json()
    df = pandas.DataFrame(r)
    print(data)



###CURRENTLY WORKING ON UI USING CUSTOMTKINTER
#window
# window = ctk.CTk()
# window.title('Squarespace Companion')
# window.geometry('600x400')

# #widgets
# label = ctk.CTkLabel(window, text = 'a ctk label',
#                         fg_color = 'red',
#                         text_color = 'white',
#                         corner_radius = 10)
# label.pack()

# button = ctk.CTkButton(window,
#                         text = 'a ctk button',
#                         fg_color = '#FF0',
#                         text_color = 'red',
#                         hover_color = '#AA0',
#                         command = lambda: ctk.set_appearance_mode('dark'))
# button.pack()

# #run
# window.mainloop()



# print('Welcome to Squarespace Companion!\n'
#       '\n'
#       'If you have not already, please configure your settings\n'
#       'under the settings option in the main menu.')
# time.sleep(3)

# #Start the menu loop
# while True:
#     print('Main menu \n')
#     print('c - Create Products \n'
#           's - Settings \n'
#           'x - Exit \n')
#     selection = input('Select an option. \n')

#     if selection == 'c':
#         getPages()
#         print('\n')

#     elif selection == 's':
#         m.settingsMenu()

#     elif selection == 'x':
#         break

#     elif selection != ['c', 's', 'x']:
#         print('not a valid selection'
#               '\n')



### Working on a version of import excel that imports .numbers files
from numbers_parser import Document
doc = Document('/Users/jonathan/Downloads/DRESS INVENTORY.numbers')
sheets = doc.sheets()
tables = sheets[0].tables()
rows = tables[0].rows()

newDict = dict(doc)

print(type(newDict))