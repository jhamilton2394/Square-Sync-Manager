"""
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
import os
import base64
from tkinter.filedialog import askopenfilename

class AuthController:
    def __init__(self):
        self.active_user = None
                    
    def login_user(self, username, password):
        """
        Called by LoginView's login method upon login attempt. Creates a temp_user then calls the User models get_user method.
        If the get_user method returns a user instance then the temp_user and the matched_users passwords are compared. If
        successful the user is assigned as active and the instance is returned to the login view.
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

    def update_user_settings(self, argument_dict, active_user):
        """
        Called by SettingsView's update_user_settings method.
        This function uses the argument dictionary to set the corresponding attributes of the
        active user using setattr(). User_list is then updated with the updated user.
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
        """Encrypts given data using the derived_key."""
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
