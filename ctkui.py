import tkinter as tk
import customtkinter

### This is the top level window
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        #add widgets here
        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

    #add methods here

### This is the main window. Widgets, methods, and top level windows can be added into this.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")

        # add widgets to app
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        # self.button.grid(row=0, column=0, padx=20, pady=10)
        self.button_1 = customtkinter.CTkButton(self, text="open toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)
        self.toplevel_window = None

    # add methods to app
    def button_click(self):
        print("button click")

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it



if __name__ == "__main__":
    app = App()

    app.mainloop()