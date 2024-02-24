import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfilename
import customtkinter
from PIL import Image, ImageTk
from controllers import *
import sys

#### In App class, leave "Create login view" block commented out for development
#### Leave the login override block un-commented as well.

"""
The class based views can be toggled in any container inside the main app class.
Each view must be passed a "parent" when instantiated so that the view_toggle
method can place the view in the correct place.
"""

class App(customtkinter.CTk):
    """
    This is the main app window. Once authenticated, the MenuView can toggle the class
    based views inside this main window.
    """

    def __init__(self, auth_controller):
        super().__init__()
        self.auth_controller = auth_controller
        self.authenticated = False
        self.active_user = None
        self.derived_session_key = None
        self.active_widget = WelcomeView(self)

        # Login override for development
        auth_user = auth_controller.login_user("carrot", "password")
        self.active_user = auth_user
        self.authenticated = True
        self.derived_session_key = self.auth_controller.derive_key("password", auth_user.salt)



        # configure window
        self.title("Squarespace Companion")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create login view
        # loginview = LoginView(self)
        # self.wait_window(loginview)

        # Menu accessed only after successful authentication from login view
        if self.authenticated:
            menu = MenuView(self)
            
    def view_toggle(self, view, *args, **kwargs):
        """
        This method toggles the class based views on or off inside their specified containers by
        checking the state of the active_widget attribute, and changing it as necessary.
        
        Example usage:

        # Toggle view on button click
        ...command=lambda: view_toggle(WelcomeView, parent=self.sidebar_frame)

        view_toggle creates an instance of the specified view class, so it is necessary to include the view's
        required argument, which is the parent container you wish the view to be created in.
        
        The above example creates an instance of the WelcomeView class inside of the sidebar_frame container.
        """
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
    """Menu view is created after successful authentication. Contains a frame with the menu buttons."""

    def __init__(self, parent):
        self.parent = parent

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(parent, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Menu logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu",
                                                 font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,10))

        if self.parent.active_user:
            self.active_user_label = customtkinter.CTkLabel(self.sidebar_frame, text=f"Welcome {self.parent.active_user.username}!")
            self.active_user_label.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Login button
        if self.parent.active_user is None:
            self.login_button = customtkinter.CTkButton(self.sidebar_frame, text="Login", width=140)
            self.login_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        else:
            self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Log out", width=140)
            self.logout_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # Create products button
        self.create_prod_button = customtkinter.CTkButton(self.sidebar_frame, text="Create Products", width = 140,
                                                          command=lambda: self.parent.view_toggle(CreateProductsView, parent))
        self.create_prod_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # Settings button
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", width = 140,
                                                       command=lambda: self.parent.view_toggle(SettingsView, parent))
        self.settings_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        # info button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="Info", width = 140,
                                                   command=lambda: self.parent.view_toggle(AlternateLogin, parent))
        self.info_button.grid(row=5, column=0, padx=20, pady=(10, 10))

class WelcomeView:
    """
    This is the welcome widget that is visible upon program startup. It Displays instructions
    or various info.

    WelcomeView objects must be instatiated with a parent argument. The parent is which app widget will
    contain the welcome view widget. To place the WelcomeView widget in the default window simply
    pass "self" as the argument. All class based views function the same way.
    """

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.announcement_box = tk.Text(parent, wrap="word", width=250, height=580)
        self.announcement_box.insert("1.0",
                                     """Welcome to Squarespace Companion!

If you have not already, please configure your settings
under the settings option in the main menu.""")
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

    def __str__(self):
        return f"{self.__class__.__name__}"

    def destroy(self):
        self.announcement_box.destroy()
        
class SettingsView():
    """Opens the settings menu when toggled."""

    def __init__(self, parent="self", *args, **kwargs):
        self.parent = parent
        self.active_user = self.parent.active_user
        if self.active_user.api_key:
            self.decrypted_api_key = self.parent.auth_controller.decrypt(self.parent.derived_session_key, self.active_user.api_key)
        else:
            self.decrypted_api_key = None

        # Create settings frame
        self.settings_frame = customtkinter.CTkScrollableFrame(parent, width=250, height=1200)
        self.settings_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", ipadx=20)

        # API key section
        self.api_label = customtkinter.CTkLabel(self.settings_frame, text="Set API key", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.api_label.grid(row=0, column=1, padx=7, pady=5, columnspan=5, sticky="w")

        # Current key label
        self.current_key_label = customtkinter.CTkLabel(self.settings_frame, text="Current API key")
        self.current_key_label.grid(row=1, column=0, pady=5, sticky="e")

        # Current key entry field
        self.current_key_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.decrypted_api_key)
        self.current_key_entry.grid(row=1, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # Column header configuration settings
        self.column_header_label = customtkinter.CTkLabel(self.settings_frame, text="Column header configuration", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.column_header_label.grid(row=3, column=1, padx=7, pady=(20, 5), columnspan=5, sticky="w")

        # Name header
        self.name_header_label = customtkinter.CTkLabel(self.settings_frame, text="Name header")
        self.name_header_label.grid(row=4, column=0, sticky="e")
        self.name_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.product_name)
        self.name_entry.grid(row=4, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # SKU header
        self.sku_header_label = customtkinter.CTkLabel(self.settings_frame, text="SKU header")
        self.sku_header_label.grid(row=5, column=0, sticky="e")
        self.sku_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.sku)
        self.sku_entry.grid(row=5, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # Item description header
        self.item_desc_header_label = customtkinter.CTkLabel(self.settings_frame, text="Item Description header")
        self.item_desc_header_label.grid(row=6, column=0, sticky="e")
        self.item_desc_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.item_desc)
        self.item_desc_entry.grid(row=6, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # Price header
        self.price_header_label = customtkinter.CTkLabel(self.settings_frame, text="price header")
        self.price_header_label.grid(row=7, column=0, sticky="e")
        self.price_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.price)
        self.price_entry.grid(row=7, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # Quantity header
        self.qty_header_label = customtkinter.CTkLabel(self.settings_frame, text="Quantity header")
        self.qty_header_label.grid(row=8, column=0, sticky="e")
        self.qty_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.qty)
        self.qty_entry.grid(row=8, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # Deleted header
        self.deleted_header_label = customtkinter.CTkLabel(self.settings_frame, text="Deleted header")
        self.deleted_header_label.grid(row=9, column=0, sticky="e")
        self.deleted_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.deleted)
        self.deleted_entry.grid(row=9, column=1, columnspan=5, padx=7, pady=5, sticky="nsew")

        # Save button
        self.save_button = customtkinter.CTkButton(self.settings_frame, text="Save",
                                                   command=self.update_user_settings)
        self.save_button.grid(row=10, column=1, columnspan=6, padx=7, pady=5, sticky="w")

        # File selection section
        self.file_selection_label = customtkinter.CTkLabel(self.settings_frame, text="Select inventory file", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.file_selection_label.grid(row=3, column=6, padx=7, pady=(20, 5), columnspan=3, sticky="w")
        self.file_selection_entry = customtkinter.CTkEntry(self.settings_frame, placeholder_text=self.active_user.file_name)
        self.file_selection_entry.grid(row=4, column=6, columnspan=5, padx=7, pady=5, sticky="nsew")
        self.file_selection_entry.configure(state="disabled")
        self.file_select_button = customtkinter.CTkButton(self.settings_frame, text="Select file", command=self.file_select)
        self.file_select_button.grid(row=5, column=6, columnspan=6, padx=7, pady=5, sticky="w")

        # Instruction box
        self.announcement_box = tk.Text(self.settings_frame, wrap="word", width=75)
        self.announcement_box.insert("1.0",
                                     """In order for Squarespace Companion to interface with your inventory spreadsheet 
it needs to know the column headers that are used. For example; if your items are 
listed in rows, you probably have data such as "name", "description", and "price", 
set as the column headers. 

The column headers that are required to be configured are: 
name 
SKU 
item description 
price 
quantity
deleted

If your inventory spreadsheet does not have columns with this info then you must 
create them. This is the minimum info needed to create new products. 

How to set the configuration: 
Input the names of your column headers in the fields above and click save. You
must type them EXACTLY as they appear on the spreadsheet. This only needs to be
done once unless you change the headers on your excel file.""")
        self.announcement_box_font = font.Font(size=17, family="Helvetica")
        self.announcement_box.config(state="disabled", font=self.announcement_box_font, bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=11, column=0, rowspan=10, columnspan=12, padx=20, pady=20, sticky="nsew")
    
    def update_user_settings(self):
        """
        Communicates with the auth_controller to update user settings, specifically the
        api key and column header settings. Blank fields are filtered out, and remaining
        fields are sent as a dictionary to the update_user_settings method,
        along with the active_user instance. Updated user set as active and SettingsView
        is refreshed.
        """
        api_key_var = self.current_key_entry.get()
        if api_key_var:
            encrypted_api_key = self.parent.auth_controller.encrypt(self.parent.derived_session_key, api_key_var)
        else:
            encrypted_api_key = None
        product_name_var = self.name_entry.get()
        sku_var = self.sku_entry.get()
        item_desc_var = self.item_desc_entry.get()
        price_var = self.price_entry.get()
        qty_var = self.qty_entry.get()
        deleted_var = self.deleted_entry.get()

        input_dict = {"api_key": encrypted_api_key,
                      "product_name": product_name_var,
                      "sku": sku_var,
                      "item_desc": item_desc_var,
                      "price": price_var,
                      "qty": qty_var,
                      "deleted": deleted_var}
        filtered_dict = self.parent.auth_controller.dict_filter(input_dict)
        updated_user = self.parent.auth_controller.update_user_settings(filtered_dict, self.parent.active_user)
        self.parent.active_user = updated_user

        # re-render the page with updated user info
        self.parent.view_toggle(SettingsView, self.parent)
        self.parent.view_toggle(SettingsView, self.parent)

    def file_select(self):
        """
        Creates a file selection window so you can pick a file.

        Calls the auth_controllers validate_file_name method to make sure the file is
        a .xlsx file. If file path is valid the path is saved to the active_user.
        """
        file_name = askopenfilename()
        updated_user = self.parent.auth_controller.validate_file_name(file_name)

        if updated_user:
            self.parent.active_user = updated_user

            self.parent.view_toggle(SettingsView, self.parent)
            self.parent.view_toggle(SettingsView, self.parent)
        else: 
            print("controller returned false")
            if not hasattr(self, 'wrong_filetype_label'):
                self.wrong_filetype_label = customtkinter.CTkLabel(self.settings_frame, text="*Please select a .xlsx (Excel) file")
                self.wrong_filetype_label.grid(row=6, column=6, columnspan=6, padx=7, pady=5, sticky="w")
                
    def destroy(self):
        #self.settings_tabview.destroy()
        self.settings_frame.destroy()

class SettingsMessageView(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Error")
        self.geometry("300x300")

        self.announcement_box = tk.Text(self, wrap="word", width=250, height=580)
        self.announcement_box.insert("1.0",
                                     """Welcome to Squarespace Companion!

If you have not already, please configure your settings
under the settings option in the main menu.""")
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

class LoginView(customtkinter.CTkToplevel):
    """
    LoginView is called automatically upon startup. All other windows are blocked
    until authentication is successful.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Login")
        self.geometry("300x300")
        self.transient(parent)
        self.grab_set()

        self.label = customtkinter.CTkLabel(self, text="Enter username and password")
        self.label.pack(pady=10)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=5)
        
        self.login_button = customtkinter.CTkButton(self, text="Login", command=lambda: self.login())
        self.login_button.pack(pady=10)
        
    def login(self):
        """
        Communicates with the auth_controller and the User model to perform user authentication.
        If authentication is successful the authenticated user instance is returned and set
        as the active_user, authenticated status is set to True, and a derived_session_key
        is created and set.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        auth_user = self.parent.auth_controller.login_user(username, password)
        if auth_user:
            self.parent.authenticated = True
            self.parent.active_user = auth_user
            self.parent.derived_session_key = self.parent.auth_controller.derive_key(password, auth_user.salt)
            self.destroy()
        else:
            if not hasattr(self, 'login_failed_label'):
                self.login_failed_label = customtkinter.CTkLabel(self, text="Username or password incorrect")
                self.login_failed_label.pack(pady=10)
            else:
                self.login_failed_label.config(text="Username or password incorrect")

class AlternateLogin:
    def __init__(self, parent):
        self.parent = parent

        self.login_frame = customtkinter.CTkScrollableFrame(parent, width=250, height=1200)
        self.login_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", ipadx=20)

        self.label = customtkinter.CTkLabel(self.login_frame, text="Enter username and password")
        self.label.pack(pady=10)

        self.username_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self.login_frame, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=5)
        
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=lambda: self.login())
        self.login_button.pack(pady=10)

    def login(self):
        """
        Communicates with the auth_controller and the User model to perform user authentication.
        If authentication is successful the authenticated user instance is returned and set
        as the active_user, and the authenticated status is set to True.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        auth_user = self.parent.auth_controller.login_user(username, password)
        if auth_user:
            self.parent.authenticated = True
            self.parent.active_user = auth_user
            self.destroy()
        else:
            if not hasattr(self, 'login_failed_label'):
                self.login_failed_label = customtkinter.CTkLabel(self, text="Username or password incorrect")
                self.login_failed_label.pack(pady=10)
            else:
                self.login_failed_label.config(text="Username or password incorrect")

    def destroy(self):
        self.login_frame.destroy()

class CreateUserView(customtkinter.CTkToplevel):
    pass

class CreateProductsView():
    """Opens the product creation interface when toggled."""

    def __init__(self, parent="self", *args, **kwargs):
        self.parent = parent

        # Create products frame
        self.products_frame = customtkinter.CTkFrame(parent, width=250, height=1200)
        self.products_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", ipadx=20)

        self.terminal_frame = customtkinter.CTkFrame(self.products_frame, width=250, height=50)
        self.terminal_frame.grid(row=10, column=3, padx=20, pady=20, sticky="nsew")

        self.terminal = tk.Text(self.terminal_frame, bg="black", fg="white")
        self.terminal.pack(fill=tk.BOTH, expand=True)
        sys.stdout=self

        print("testing \n" * 100)
    def write(self, text):
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # Required for stdout redirection

        
    def destroy(self):
        self.products_frame.destroy()
    

class Terminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Terminal")
        self.geometry("600x400")

        self.text_widget = tk.Text(self, bg="black", fg="white")
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Redirect stdout
        sys.stdout = self

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # Required for stdout redirection