###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts as cp
import json
import keys as k
import requests
import pandas
import tkinter as tk
import customtkinter as ctk


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

getPages()



###CURRENTLY WORKING ON UI USING CUSTOMTKINTER
# #window
# window = ctk.CTk()
# window.title('Squarespace Companion')
# window.geometry('600x400')

#widgets
label = ctk.CTkLabel(window, text = 'a ctk label',
                        fg_color = 'red',
                        text_color = 'white',
                        corner_radius = 10)
label.pack()

# button = ctk.CTkButton(window,
#                         text = 'a ctk button',
#                         fg_color = '#FF0',
#                         text_color = 'red',
#                         hover_color = '#AA0',
#                         command = lambda: ctk.set_appearance_mode('dark'))
# button.pack()

# #run
# window.mainloop()