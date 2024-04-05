import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfilename
import customtkinter
from PIL import Image, ImageTk
from controllers import *
import sys
import markdown2
import html2text


#### In App class, leave "Create login view" block commented out for development
#### Leave the login override block un-commented as well.

"""
The class based views can be toggled in any container inside the main app class.
Each view must be passed a "parent" when instantiated so that the view_toggle
method can place the view in the correct place.
"""
class BaseView:
    """
    BaseView provides methods for displaying the content of markdown files.

    methods:

    load_markdown_file(self, filename):
        Opens markdown file.

    display_markdown_file(self, filename, widget):
        Inserts markdown file content into specified widget.
    """
    def __init__(self):
        pass

    def load_markdown_file(self, filename):
        """
        Opens specified file.
        """
        with open(filename, 'r') as file:
            markdown_content = file.read()
        return markdown_content

    def display_markdown_file(self, filename, widget):
        """
        Inserts markdown content into specified widget

        Parameters:
        filename: Str | path to mardown file
        widget: Tk object | widget to insert markdown into.
        """
        markdown_content = self.load_markdown_file(filename)
        html_content = markdown2.markdown(markdown_content)
        plain_text = html2text.html2text(html_content)
        widget.insert(tk.END, plain_text)

class App(customtkinter.CTk):
    """
    This is the main app window. Once authenticated, the MenuView can toggle the class
    based views inside this main window.

    Attributes:
    auth_controller: AuthController | AuthController instance, handles authentication and user business logic.
    api_controller: APIController | APIController instance, handles api business logic.
    authenticated: Bool | indicates authentication status.
    active_user: User | User instance set after successfull authentication
    derived_session_key: bytes | base64 urlsafe b64encoded key. Created using user password and salt upon login.
    decrypted_api_key: Str | decrypted api key used for api requests.
    active_widget: view object | Active view in App window. Defaults to WelcomeView

    Methods:
    view_toggle(self, view, *args, **kwargs):
        Used to toggle views inside the main app window.
    """

    def __init__(self, auth_controller):
        super().__init__()
        self.auth_controller = auth_controller
        self.api_controller = None
        self.authenticated = False
        self.active_user = None
        self.derived_session_key = None
        self.decrypted_api_key = None
        self.active_widget = WelcomeView(self)

        # # Login override for development
        # auth_user = auth_controller.login_user("carrot", "password")
        # self.active_user = auth_user
        # self.authenticated = True
        # self.derived_session_key = self.auth_controller.derive_key("password", auth_user.salt)
        # # decrypt api key for development mode
        # dec_key = auth_controller.decrypt(self.derived_session_key, self.active_user.api_key)
        # self.active_user.api_key = dec_key
        # # create api controller
        # self.api_controller = APIController(auth_user)

        # configure window
        self.title("Square Sync Manager v0.0.3.1")
        self.geometry(f"{1100}x{580}")

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
    """
    Menu view is created after successful authentication. Contains a frame with the menu buttons.
    
    Attributes:
    parent: View object | The view that contains MenuView. Can be any view class, but is typically an instance of App.

    Methods:
    logout(self):
        Logs you out by destroying the main app window.

    change_appearance_mode_event(self, new_appearance_mode):
        Changes appearance mode.    
    """

    def __init__(self, parent):
        self.parent = parent

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(parent, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

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
            self.logout_button = customtkinter.CTkButton(self.sidebar_frame, text="Log out", width=140,
                                                         command=self.logout)
            self.logout_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # Create products button
        self.create_prod_button = customtkinter.CTkButton(self.sidebar_frame, text="Create Products", width = 140,
                                                          command=lambda: self.parent.view_toggle(CreateProductsView, parent))
        self.create_prod_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # Settings button
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", width = 140,
                                                       command=lambda: self.parent.view_toggle(SettingsView, parent))
        self.settings_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        # Info button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="Info", width = 140,
                                                   command=lambda: self.parent.view_toggle(InfoView, parent))
        self.info_button.grid(row=5, column=0, padx=20, pady=(10, 10))

        # License button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="License", width = 140,
                                                   command=lambda: self.parent.view_toggle(LicenseView, parent))
        self.info_button.grid(row=6, column=0, padx=20, pady=(10, 10))

        # copyright label logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Copyright © 2024 Jonathan Hamilton")
        self.logo_label.grid(row=8, column=0, padx=20, pady=(20,10))



    def logout(self):
        """
        Logs the user out by destroying the main app window.
        """
        self.parent.destroy()

    def change_appearance_mode_event(self, new_appearance_mode):
        """
        Changes appearance mode. Options are "light", "dark", and "system".
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

class WelcomeView(BaseView):
    """
    This is the welcome widget that is visible upon program startup. It Displays instructions
    or various info.
    """

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.announcement_box = tk.Text(parent, wrap="word", width=250, height=580)
        self.display_markdown_file("files/welcome.md", self.announcement_box)
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

    def __str__(self):
        return f"{self.__class__.__name__}"

    def destroy(self):
        self.announcement_box.destroy()

class LicenseView(BaseView):
    """This view displays the current license."""

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.announcement_box = tk.Text(parent, wrap="word", width=250, height=580)
        self.display_markdown_file("License", self.announcement_box)
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

    def __str__(self):
        return f"{self.__class__.__name__}"

    def destroy(self):
        self.announcement_box.destroy()

class InfoView(BaseView):
    """
    Info View displays info about the app. In the current case it displays the content of
    the readme.MD file.
    """
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.announcement_box = tk.Text(parent, wrap="word", width=250, height=580)
        self.display_markdown_file("README.md", self.announcement_box)
        self.announcement_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.announcement_box.tag_configure("custom tag", foreground="white")
        self.announcement_box.tag_add("custom tag", 0.0, "end")
        self.announcement_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")


    def __str__(self):
        return f"{self.__class__.__name__}"

    def destroy(self):
        self.announcement_box.destroy()
        
class SettingsView(BaseView):
    """
    Opens the settings menu when toggled.
    
    Attributes:
    parent: view class | the view that contains the settings view.
    active_user: User | The active user. Makes user info accessible to the view.
    decrypted_api_key: Str | active users decrypted api key.

    Methods:
    update_user_settings(self):
        Gets data from entry fields and saves it to user profile.

    file_select(self):
        Creates a file selection window so you can pick a file.
    """

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
        self.display_markdown_file("files/settings_tut.md", self.announcement_box)
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
            # session api_controller is immediately updated
            self.parent.api_controller.api_key = api_key_var
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

class LoginView(customtkinter.CTkToplevel):
    """
    LoginView is called automatically upon startup. All other windows are blocked
    until authentication is successful.

    Methods:
    login(self):
        Gets username and password from entry fields and sends it to the auth_controller.

    create_user(self):
        Toggles the create_user view.   
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

        self.create_user_button = customtkinter.CTkButton(self, text="Create new user", command=self.create_user)
        self.create_user_button.pack(pady=5)
        
    def login(self):
        """
        Communicates with the auth_controller and the User model to perform user authentication.
        If authentication is successful the authenticated user instance is returned and set
        as the active_user, authenticated status is set to True, and a derived_session_key
        is created and set. The API controller is also created.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        auth_user = self.parent.auth_controller.login_user(username, password)
        if auth_user:
            self.parent.authenticated = True
            self.parent.active_user = auth_user
            self.parent.derived_session_key = self.parent.auth_controller.derive_key(password, auth_user.salt)
            self.parent.api_controller = APIController(auth_user)
            if auth_user.api_key:
                self.parent.api_controller.api_key = self.parent.auth_controller.decrypt(self.parent.derived_session_key, auth_user.api_key)
                self.parent.api_controller.set_store_pages_info()
            self.destroy()
        else:
            if not hasattr(self, 'login_failed_label'):
                self.login_failed_label = customtkinter.CTkLabel(self, text="Username or password incorrect")
                self.login_failed_label.pack(pady=10)
            else:
                self.login_failed_label.configure(text="Username or password incorrect")
    
    def create_user(self):
        """Toggles the CreateUserView"""
        self.create_user_window = CreateUserView(self.parent)
        #self.legal_window = LegalDocsView(self.parent)
class AlternateLogin: # Not in use
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
    """
    View for creating a new user profile.

    Methods:
    create_user(self):
        Gets user info from entry fields and sends it to the auth_controller to create a new user.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Create new user")
        self.geometry("300x300")
        self.transient(parent)
        self.grab_set()

        self.label = customtkinter.CTkLabel(self, text="Enter username and password")
        self.label.pack(pady=10)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(self, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=5)

        self.password_reentry = customtkinter.CTkEntry(self, show="*", placeholder_text="Re-enter password")
        self.password_reentry.pack(pady=5)

        self.create_user_button = customtkinter.CTkButton(self, text="Create user", command=self.create_user)
        self.create_user_button.pack(pady=10)

    def create_user(self):
        """Communicates with the auth_controller to create a new user."""
        self.password_match = False
        username = self.username_entry.get()
        password = self.password_entry.get()
        password2 = self.password_reentry.get()

        create_attempt = self.parent.auth_controller.create_new_user(username, password, password2)

        if not hasattr(self, 'message_label'):
            self.message_label = customtkinter.CTkLabel(self, text=f"{create_attempt}")
            self.message_label.pack(pady=10)
        else:
            self.message_label.configure(text=f"{create_attempt}")

class LegalDocsView(customtkinter.CTkToplevel, BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent=parent
        self.title("EULA and Privacy Policy agreement")
        self.geometry=("1000x1000")
        self.transient(parent)
        self.grab_set()

        # # scrollable main frame
        # self.main_frame = customtkinter.CTkFrame(self, width=600, height=400)
        # self.main_frame.pack()

        # # Create EULA frame
        # self.eula_frame = customtkinter.CTkScrollableFrame(self.main_frame, width=300, height=300)
        # self.eula_frame.pack()

        # Create EULA box
        self.eula_box = tk.Text(self, wrap="word")
        self.display_markdown_file("files/EULA.md", self.eula_box)
        self.eula_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.eula_box.tag_configure("custom tag", foreground="white")
        self.eula_box.tag_add("custom tag", 0.0, "end")
        self.eula_box.pack(padx=20, pady=20)
        # self.eula_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

        # Create privacy policy frame
        # self.pp_frame = customtkinter.CTkScrollableFrame(self.main_frame, width=300, height=300)
        # self.pp_frame.pack()

        # Create privacy policy box
        self.pp_box = tk.Text(self, wrap="word")
        self.display_markdown_file("files/privacy_policy.md", self.pp_box)
        self.pp_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.pp_box.tag_configure("custom tag", foreground="white")
        self.pp_box.tag_add("custom tag", 0.0, "end")
        self.pp_box.pack(padx=20, pady=20)
        # self.pp_box.grid(row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

        # Create checkboxes
        self.eula_checkbox = customtkinter.CTkCheckBox(self, text="I have read and agree to the End User License Agreement",)
        self.eula_checkbox.pack(anchor="w", padx=20, pady=10)
        self.pp_checkbox = customtkinter.CTkCheckBox(self, text="I have read and agree to the Privacy Policy")
        self.pp_checkbox.pack(anchor="w", padx=20, pady=10)


class CreateProductsView:
    """
    Opens the product creation interface when toggled.

    Attributes:
    parent: view class | The view that contains createProductsView.
    pages: List | A list of dictionaries; [{title: page title, id: page id}, ...]

    Methods:
    page_select(self):
        Sets the auth_controllers pageID attribute to the selected page.

    create_all(self):
        Initiates product creation process if all conditions are met.

    write(self, text):
        Performs write action for local terminal.

    flush(self):
        Required for stdout redirection.
    """

    def __init__(self, parent="self", *args, **kwargs):
        self.parent = parent
        self.pages = self.parent.api_controller.page_ids()

        # Create products frame
        self.products_frame = customtkinter.CTkFrame(parent, width=250, height=1200)
        self.products_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", ipadx=20)

        # Create frame to contain terminal
        self.terminal_frame = customtkinter.CTkFrame(self.products_frame, width=250, height=50)
        self.terminal_frame.grid(row=10, rowspan=20, column=3, padx=20, pady=20, sticky="nsew")

        # Create output terminal
        self.terminal = tk.Text(self.terminal_frame, bg="black", fg="white")
        self.terminal.pack(fill=tk.BOTH, expand=True)
        sys.stdout=self

        # Selected file label
        self.selected_file_label = customtkinter.CTkLabel(self.products_frame, text="Selected inventory file")
        self.selected_file_label.grid(row=31, column=3, padx=7, pady=1, sticky="w")
        
        # Selected file display box
        self.file_name_box = tk.Text(self.products_frame, wrap="word", height=5)
        self.file_name_box.insert("1.0", f"{self.parent.active_user.file_name}")
        self.file_name_box.config(state="disabled", font="Helvetica", bg="#2b2d30")
        self.file_name_box.tag_configure("custom tag", foreground="white")
        self.file_name_box.tag_add("custom tag", 0.0, "end")
        self.file_name_box.grid(row=32, column=3, padx=7, pady=2, sticky="w")

        # Create upload button
        self.upload_button = customtkinter.CTkButton(self.products_frame, width=140, text="Upload to site",
                                                     command=self.create_all)
        self.upload_button.grid(row=33, column=3, padx=7, pady=2, sticky="w")

        # Create page select label
        self.radio_frame_label = customtkinter.CTkLabel(self.products_frame, text="Page Select")
        self.radio_frame_label.grid(row=10, column=4, padx=20, pady=0, sticky="nsew")

        # Create radio button frame
        self.radio_frame = customtkinter.CTkFrame(self.products_frame, width=150, height=100)
        self.radio_frame.grid(row=11, column=4, padx=20, pady=7, sticky="nsew")

        # Create page select radio buttons. Pages and their ID's are retreived from api controller and looped over.
        self.selected_option = tk.IntVar()

        if self.pages:
            for i, page in enumerate(self.pages):
                self.option = customtkinter.CTkRadioButton(self.radio_frame, variable=self.selected_option, value=i, text=page["title"],
                                                        command= self.page_select)
                self.option.grid(row=10, column=10, rowspan=2, padx=20, pady=10)
        elif self.pages == False:
            self.no_conn_label = customtkinter.CTkLabel(self.radio_frame, text="Not connected to internet")
            self.no_conn_label.grid(row=10, column=10, rowspan=2, padx=20, pady=10)
        elif self.pages == None:
            self.no_conn_label = customtkinter.CTkLabel(self.radio_frame, text="There are no pages to select")
            self.no_conn_label.grid(row=10, column=10, rowspan=2, padx=20, pady=10)

    def page_select(self):
        """
        Gets selected page from the radio button list and sets it as the pageID in the
        auth_controller instance.
        """
        self.selected_index = self.selected_option.get()
        self.page_dict = self.pages[self.selected_index]
        self.parent.api_controller.pageID = self.page_dict["id"]
        print(f'Page "{self.page_dict["title"]}"{self.page_dict["id"]}')

    def create_all(self):
        """Initiates product creation process if all conditions are met."""

        if self.parent.api_controller.store_pages_info == None:
            self.parent.api_controller.set_store_pages_info()
            self.parent.view_toggle(CreateProductsView, self.parent)
            self.parent.view_toggle(CreateProductsView, self.parent)
        elif self.parent.api_controller.pageID == None:
            print("You must select a page to upload to")
        else:
            self.parent.api_controller.createAllProducts()

    def write(self, text):
        """Performs write action for local terminal."""
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)  # Scroll to the end

    def flush(self):
        """Required for stdout redirection"""
        pass
 
    def destroy(self):
        self.products_frame.destroy()