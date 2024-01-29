import tkinter as tk
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Squarespace Companion")
        self.geometry(f"{1100}x{580}")
        self.toplevel_window = None

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Menu logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu",
                                                 font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,10))
        
        # Create products button
        self.create_prod_button = customtkinter.CTkButton(self.sidebar_frame, text="Create Products", width = 140)
        self.create_prod_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Settings button
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", width = 140,
                                                       command=self.open_toplevel_settings)
        self.settings_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # info button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="Info", width = 140)
        self.info_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # create second sidebar frame for practice
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=200, corner_radius=2)
        self.sidebar_frame2.grid(row=0, column=2, rowspan=4, padx=40,  sticky="nsew")
        self.input_button = customtkinter.CTkButton(self.sidebar_frame2, text="click for input", command=self.input_dialog_event)
        self.input_button.grid(row=0, column=0, padx=20, pady=10)

        # create text
        self.announcement_box = tk.Text(self, wrap="word", width=250)
        self.announcement_box.insert("1.0",
                                     '''Welcome to Squarespace Companion!

If you have not already, please configure your settings
under the settings option in the main menu.''')
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")


    def input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="input here", title="dialog box")
        print(dialog.get_input())

    def submit_button_event(self, event=None):
        input = self.entry.get()
        self.entry.delete(0, 100)
        if input == '':
            None
        else:
            print(input)

    def open_toplevel_settings(self):
        '''
        Method opens the settingss menu if its not already open.
        '''
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow_settings(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.hide_all_body()

    def hide_all_body(self):
        '''
        Hides all main body widgets. Used to switch between widgets. Button click should call this method
        then call method to make desired widget visible.

        Any newly created body widgets should be added here so they can be hidden when needed.
        '''
        self.announcement_box.grid_forget()

class ToplevelWindow_settings(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1100x580")
        self.title('Settings Menu')

        #add widgets here
        self.settings_tabview = customtkinter.CTkTabview(self, width=1100, height=580)
        self.settings_tabview.grid(row=0,column=0, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()