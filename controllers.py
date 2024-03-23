"""
A controller module that acts as the middle man between the views and the models.

This module is designed to accompany the model_auth_user module. Together they
can act as a stand-alone authentication-user model system.

Note: Any data encrypted with this system is permenantly lost if the user forgets their password.
Creating a recovery system is not a priority at this time since the only data intended for
encryption, as of now, is the api key which can easily be retreived from the squarespace
website if the user does forget their password here.
"""


from model_auth_user import *
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import requests
import json
from pandas import ExcelFile
import urllib.request

class AuthController:
    """
    Controls user authentication and user CRUD operations.

    Attributes:
    active_user: User | The authenticated user

    Methods:
    login_user(self, username, password):
        Logs in the specified user if the password is correct.

    validate_password(user, password):
        Checks if entered password matches the users password.

    update_user_settings(self, argument_dict, active_user):
        Updates and saves the users settings.

    derive_key(self, password, salt):
        Creates a derived encryption key.

    encrypt(self, key, data):
        Encrypts data.

    decrypt(self, key, encrypted_data):
        Decrypts data.

    validate_file_name(self, file_name):
        Checks if file is .xlsx. Saves to user settings if True.

    dict_filter(self, dict):
        Filters out empty key value pairs from a dictionary.
    """
    def __init__(self):
        """Initialize the controller in the main file, and pass it to the App() class so the views can access the controller."""
        self.active_user = None
                    
    def login_user(self, username, password):
        """
        Creates a temp_user then calls the User model's get_user method.
        If the get_user method returns a user instance then the temp_user and the matched_users passwords are compared. If
        successful the user is assigned as active and the instance is returned.

        Returns:
        matched_user: User | The matched user object from storage.
        """
        temp_user = User(username, password)
        matched_user = temp_user.get_user()
        if matched_user:
            if matched_user.password == temp_user.password:
                self.active_user = matched_user
                return matched_user
            else:
                return False
        else:
            return False
        
    def validate_password(user, password):
        """
        Takes a user instance and password and checks if given password matches the
        instance's password hash.

        Note: The user instance cannot be a temp_user.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == user.password:
            return True
        else:
            return False

    def password_match(self, password1, password2):
        if password1 == password2:
            return True
        else:
            return False
        
    def create_new_user(self, username, password1, password2):
        if self.password_match(password1, password2):
            new_user = User(username, password1)
            if new_user.save():
                return "New user created successfully"
            else:
                return "Username already taken"
        else:
            return "Passwords do not match"

    def update_user_settings(self, argument_dict, active_user):
        """
        This function uses the argument dictionary to set the corresponding attributes of the
        active user using setattr(). User_list is then updated with the updated user.

        Parameters:
        argument_dict: dict | A dictionary containing user attributes
        active_user: User | The active_user for the session.

        Returns:
        active_user: User | The updated active user.
        """
        for key, value in argument_dict.items():
            setattr(active_user, key, value)

        user_list = active_user.get_user_list()

        for user in user_list:
            if active_user.username == user.username:
                user_list.remove(user)
        user_list.append(active_user)
        active_user.save_user_list(user_list)
        return active_user

    def derive_key(self, password, salt):
        """
        Creates a derived encryption key using the users password and the users
        randomly generated salt. Used in the encrypt and decrypt methods.

        Parameters:
        password: str | The users plain-text password (obtained during login)
        salt: bytes | The users salt attribute

        Returns:
        key: bytes | base64 urlsave b64encoded key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return base64.urlsafe_b64encode(key)
    
    def encrypt(self, key, data):
        """
        Encrypts given data using the derived_key.
        
        Parameters:
        key: bytes | derived key from derive_key() method.
        data: str | data to encrypt. If you need to encrypt a dict, change it to a string first.

        Returns:
        encrypted_data: bytes
        """
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data
    
    def decrypt(self, key, encrypted_data):
        """Decrypts given encrypted data using the derived_key."""
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data
    
    def validate_file_name(self, file_name):
        """
        Checks if given file path ends in .xlsx.

        If the file is an excel file then it is valid, and is saved to the active_user's profile.

        Parameters:
        file_name: str | file path

        Returns:
        user instance updated with file_name attribute, or False if file_name is not .xlsx.
        """
        if file_name.endswith('.xlsx'):
            input_dict = {"file_name": file_name}
            filtered_dict = self.dict_filter(input_dict)
            updated_user = self.update_user_settings(filtered_dict, self.active_user)
            return updated_user
        else:
            print("file name does not end with .xlsx")
            return False
        
    def dict_filter(self, dict):
        """
        Filters out any key value pairs with a None or equivalent value.

        Parameters:
        dict: dict | any dictionary

        Returns:
        A new dictionary with any empty key value pairs removed.
        """
        filtered_dict = {}
        for key, value in dict.items():
            if value:
                filtered_dict[key] = value
        return filtered_dict

class APIController:
    """
    The current API methods can be broken down into product methods, and store_pages methods.

    Product methods:
    createProduct: Posts a single product
    createAllProducts: Parses data from excel sheet and passes it to createProduct. Creates all products on excel sheet.
    getProducts: Gets the initial page of product info.
    siteMasterProdList: Uses getProducts to create a list of all products on site. Uses pagination as necesary.

    store_pages methods:
    get_store_pages_info: Gets the initial page of store_pages info.
    set_store_pages_info: Calls get_store_pages_info and saves return value to the attribute "store_pages_info".
    page_ids: Filters the store_pages_info attribute for "title" and "id". Returns a list of pages with their titles and id's.
        Need to incorporate pagination
    """
    def __init__(self, user):
        
        self.api_key = user.api_key
        self.nameHeader = user.product_name
        self.skuHeader = user.sku
        self.item_desc_header = user.item_desc
        self.priceHeader = user.price
        self.qtyHeader = user.qty
        self.delHeader = user.deleted
        self.filePath = user.file_name
        self.pageID = None

        self.store_pages_info = None

    def check_connection(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host) #Python 3.x
            return True
        except:
            # print("You are not connected to the internet.")
            return False

    def createProduct(self, storePageID, productName, productDescription, variantSku, productPrice, quantity):
        if self.check_connection():
            dataOutbox = {'type': 'PHYSICAL',
                    'storePageId': storePageID,
                    'name': productName,
                    'description': productDescription,
                    'isVisible': 'true',
                    'variants': [{'sku': variantSku,
                                    'pricing': {'basePrice': {'currency': 'USD',
                                                            'value': productPrice
                                                            }
                                                },
                                    'stock': {'quantity': quantity}}
                                    ]
                        }
            jsonDataOutbox = json.dumps(dataOutbox)
            prodURL = 'https://api.squarespace.com/1.0/commerce/products'
            prodHeaders = {'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': 'APIAPP1.0',
                    'Content-Type': 'application/json'}
            r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
            json_data = r.json()
            pretty_json_data = json.dumps(json_data, indent=3)
            print(r)
            print(pretty_json_data)
            return
        else:
            return False

    def createAllProducts(self):
        """
        Converts excel sheet to pandas dataframe. Extracts data from specified columns and passes
        it to the createProduct method.
        """
        if self.check_connection():
            xls = ExcelFile(self.filePath)
            df = xls.parse(xls.sheet_names[0])
            product_list = self.site_master_prod_list()
            #loop thru doc & create products using column header files.
            for i in range(len(df)):
                sku = str((df.loc[i].at[self.skuHeader]))
                name = (df.loc[i].at[self.nameHeader])
                itemDesc = (df.loc[i].at[self.item_desc_header])
                price = str((df.loc[i].at[self.priceHeader]))
                quant = str((df.loc[i].at[self.qtyHeader]))
                del2 = (df.loc[i].at[self.delHeader])
                pageID = self.pageID
                if name in product_list:
                    print(name, 'already on site, skipping...\n')
                elif del2 == 'x':
                    print(name, 'previously deleted from site by user, skipping...')
                else:
                    self.createProduct(storePageID=pageID,
                                    productName=name,
                                productDescription=itemDesc,
                                variantSku=sku,
                                productPrice=price,
                                quantity=quant)
                
    def site_master_prod_list(self):
        if self.check_connection():
            #Initial product query
            actual_prod_list = []
            ###Commenting out 2 lines below, which just opens the data file. The file was used for testing purposes.
            # open_product_data = open('product_file', 'r')
            # raw_data = open_product_data.read()
            raw_data = self.getProducts()
            prod_main_dict = json.loads(raw_data)
            prod_list = prod_main_dict['products']
            pagination = prod_main_dict['pagination']
            cursor = pagination['nextPageCursor']
            for i in prod_list:
                actual_prod_list.append(i['name'])
            ###Loops through all pages if they exist.
            while pagination['hasNextPage'] == True:
                raw_data = self.getProducts(cursor)
                prod_main_dict = json.loads(raw_data)
                prod_list = prod_main_dict['products']
                pagination = prod_main_dict['pagination']
                cursor = pagination['nextPageCursor']
                for i in prod_list:
                    actual_prod_list.append(i['name'])
            return actual_prod_list
        
    def getProducts(self, cursor=''):
        if self.check_connection():
            prodURL = 'https://api.squarespace.com/1.0/commerce/products?cursor=' + cursor
            prodHeaders = {'Authorization': 'Bearer ' + self.api_key,
                        'User-Agent': 'APIAPP1.0'}
            r = requests.get(prodURL, headers=prodHeaders)
            json_data = r.json()
            pretty_json_data = json.dumps(json_data, indent=3)
            return pretty_json_data
        else:
            return False
    
    def get_store_pages_info(self):
        """
        Uses the squarespace store_pages api to get a dictionary of the store
        pages data. Dictionary contains pagination data, and a list of store
        pages and their id's.
        """
        if self.check_connection():
            store_pages_URL = 'https://api.squarespace.com/1.0/commerce/store_pages'
            headers = {'Authorization': 'Bearer ' + self.api_key,
                    'User-Agent': 'APIAPP1.0'}
            r = requests.get(store_pages_URL, headers=headers)
            data = r.json()
            return data
        else:
            return None
    
    def set_store_pages_info(self):
        """
        Gets the store pages info and sets it as an attribute for use during
        the session.
        """
        self.store_pages_info = self.get_store_pages_info()

    def page_ids(self):
        """
        Filters page names and id's from the store_pages_info
        attribute. Set_store_pages_info must be called first.

        Returns: list | [{title: page title, id: page id}, ...]
        """
        if self.check_connection() and self.store_pages_info:
            pages_list = []
            try:
                for page in self.store_pages_info["storePages"]:
                    pages_dict = {}
                    id_value = page["id"]
                    title_value = page["title"]
                    pages_dict["title"] = title_value
                    pages_dict["id"] = id_value
                    pages_list.append(pages_dict)
                return pages_list
            except KeyError:
                print("There are no store pages to upload to")
                return None
        return False
    
