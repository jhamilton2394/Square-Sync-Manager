import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
from functools import wraps


class App(customtkinter.CTk):
    '''
    This is the main app window.
    '''
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Squarespace Companion")
        self.geometry(f"{1100}x{580}")
        self.active_widget = None
        self.authenticated = False

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create login view
        loginview = LoginView(self)
        self.wait_window(loginview)

        # Menu accessed only after successful authentication from login view
        if self.authenticated:
            menu = MenuView(self)
            
            # Create the default view
            welcomeview = WelcomeView(self)

    def view_toggle(self, view, *args, **kwargs):
        '''
        This method toggles the class based views on or off inside their specified containers.
        
        Example usage:

        # Toggle view on button click
        ...command=lambda: view_toggle(WelcomeView(parent=self.sidebar_frame))

        view_toggle creates an instance of the class view, so it is necessary to include the class view's
        required argument, which is the parent container you wish the view to be created in.
        
        The above example creates an instance of the WelcomeView class inside of the sidebar_frame container.
        '''

        if self.active_widget is None:
            self.view = view(*args, **kwargs)
            self.active_widget = self.view
        elif isinstance(self.active_widget, view):
            self.active_widget.destroy()
            self.active_widget = None
        elif self.active_widget is not None or isinstance(self.active_widget, view):
            self.active_widget.destroy()
            self.view = view(*args, **kwargs)
            self.active_widget = self.view

class MenuView(customtkinter.CTk):
    '''
    Menu view is created after successful authentication. Contains a frame with the menu buttons.
    '''

    def __init__(self, parent):
        self.parent = parent

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(parent, width=180, corner_radius=0)
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
                                                       command=lambda: parent.view_toggle(SettingsView, parent=parent))
        self.settings_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # info button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="Info", width = 140,
                                                   command=lambda: parent.view_toggle(WelcomeView, parent=self.sidebar_frame))
        self.info_button.grid(row=3, column=0, padx=20, pady=(10, 10))


class WelcomeView:
    '''
    This is the welcome widget that is visible upon program startup. It Displays instructions
    or various info.

    WelcomeView objects must be instatiated with a parent argument. The parent is which app widget will
    contain the welcome view widget. To place the WelcomeView widget in the default window simply
    pass "self" as the argument. All class based views function the same way.
    '''
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.announcement_box = tk.Text(parent, wrap="word", width=250)
        self.announcement_box.insert("1.0",
                                     '''Welcome to Squarespace Companion!

If you have not already, please configure your settings
under the settings option in the main menu.''')
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Create test button
        self.test_button = customtkinter.CTkButton(parent, text="Test button", width=140)
        self.test_button.grid(row=1, column=1)

    def __str__(self):
        return f"{self.__class__.__name__}"

    def destroy(self):
        self.announcement_box.destroy()
        self.test_button.destroy()

class SettingsView:

    '''
    Example text
    '''

    def __init__(self, parent="self", *args, **kwargs):
        self.parent = parent
        self.settings_tabview = customtkinter.CTkTabview(parent, width=250)
        self.settings_tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.settings_tabview.add("Set API Key")
        self.settings_tabview.add("Select Inventory File")
        self.settings_tabview.add("Column Header Configuration")

        # Create API key entry field and button
        self.entry_button = customtkinter.CTkButton(self.settings_tabview.tab("Set API Key"), text="Save", width=80)
        self.entry_button.grid(row=0, column=0, padx=5, pady=20)
        self.entry = customtkinter.CTkEntry(self.settings_tabview.tab("Set API Key"), placeholder_text="API Key", width=250)
        self.entry.grid(row=0, column=1, pady=20)

    def destroy(self):
        self.settings_tabview.destroy()

class LoginView(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Login")
        self.geometry("300x300")
        self.transient(parent)
        self.grab_set()

        self.label = customtkinter.CTkLabel(self, text="Enter username and password")
        self.label.pack(pady=10)

        # self.usernname_label = customtkinter.CTkLabel(self, text="Username")
        # self.usernname_label.pack()
        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=5)
        
        self.login_button = customtkinter.CTkButton(self, text="Login", command= self.authenticate)
        self.login_button.pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.parent.authenticated = True
        self.destroy()