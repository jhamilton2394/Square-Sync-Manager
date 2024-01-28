'''
If using Ubuntu you must run the following before being able to use tkinter:

sudo apt-get install python3.11-tk

The out-of-the-box tkinter doesn't seem to work on Ubuntu without being explicitly installed with apt-get.
'''

import tkinter as tk
import customtkinter
import menu as m

### UI structure:
#   Windows are separeted into their own classes. The class 'App' is the main program window that will house
#   the main menu. Each menu button will get its own class, and so on and so forth for sub menu buttons.


### This is the top level window
class ToplevelWindow_settings(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.title('Settings menu')

        #add widgets here
        # self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        # self.label.pack(padx=20, pady=20)
        self.button_1 = customtkinter.CTkButton(self, text='Set API Key', command=m.apiKeyInput)
        self.button_2 = customtkinter.CTkButton(self, text='Select Inventory File', command=m.inventory_file_select)

        #Widget placement
        self.button_1.grid(row=0, column=0, padx=20, pady=20)
        self.button_2.grid(row=1, column=0, padx=20, pady=20)

    #add methods here

### This is the main window. Widgets, methods, and top level windows can be added into this.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")

        # add widgets to app

        #create buttons
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        # self.button.grid(row=0, column=0, padx=20, pady=10)
        self.button_1 = customtkinter.CTkButton(self, text="Settings", command=self.open_toplevel_settings)
        self.button_2 = customtkinter.CTkButton(self, text="open toplevel 1", command=self.open_toplevel_1)

        #place buttons
        self.button_1.grid(row=0, column=0, padx=20, pady=20)
        self.button_2.grid(row=1, column=0, padx=20, pady=20)
        self.toplevel_window = None

    # add methods to app
    def button_click(self):
        print("button click")

    def open_toplevel_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow_settings(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_toplevel_1(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it



if __name__ == "__main__":
    app = App()

    app.mainloop()