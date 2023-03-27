import tkinter as tk
import customtkinter
from menu import settingsMenu, apiKeyInput

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

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")

        # add widgets to app
        self.button = customtkinter.CTkButton(self, text="Settings", command=settingsMenu)
        self.button1 = customtkinter.CTkButton(self, text="About", command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=10)
        self.button1.grid(row=1, column=0, padx=20, pady=10)

    # add methods to app
    def button_click(self):
        print("button click")

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
                
    def settingsMenuOptions():
        



app = App()
app.mainloop()