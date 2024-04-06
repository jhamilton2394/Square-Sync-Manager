# Written by Jonathan Hamilton

"""
A secure pickle based user model

This module along with its controller can act as a stand-alone authentication-user model system. It contains tools for
creating users with secure passwords, as well encrypting and decrypting sensitive data. Users are saved to the
local machines file system via pickling, but this can be easily modified to work with SQL and an ORM.
"""

import hashlib
import pickle
import os
import platform
from pathlib import Path


class User:
    """
    Create a user with a username and password.
    
    Password is only saved as a hash. Refer to SecurePassword class for password details. Any users created
    are temp_users until the username can be validated. Once validated the user is saved and becomes a
    regular user.

    Usage:
    # Create a new user.
    new_user = User("username", "password")
    new_user.save()

    Attributes:
    username: str | username
    password: str | Hash of users plain-text password, stored as string.
    salt: bytes | Randomly generated value used for encryption.

    File header settings: str | The following attributes are used to configure the users inventory sheet api:
    api_key, product_name, sku, item_desc, price, qty, deleted, file_name

    Methods:
    validate_username(self):
        Checks if the username already exists.

    save(self):
        Saves the user object to the users file if username is valid.

    get_user(self):
        Uses temp_user object to retreive actual user from storage.

    get_user_list(self):
        Uses any user object to retreive user_list from storage.

    save_user_list(self, user_list):
        Saves user_list to users file. 
    """

    def __init__(self, username: str, password: str):
        """
        Initialize the user with a username, password, and randomly generated salt.

        Parameters:
        username: str | desired username
        password: str | desired password
        """
        self.username = username
        self.password = str(SecurePassword(password))
        self.salt = os.urandom(16)

        self.api_key = None
        self.product_name = None
        self.sku = None
        self.item_desc = None
        self.price = None
        self.qty = None
        self.deleted = None

        self.program_directory = self.set_program_directory()
        self.user_file_path = os.path.join(self.program_directory, "users.pkl")
        self.file_name = None

    def validate_username(self):
        """
        Checks if username already exists.
        
        Returns False if username exists, ie username is NOT valid. Returns True if username
        does not exist, ie username IS valid.

        Also checks if the file containing user data exists. If not, then no users yet exist and
        the function returns True.
        """
        file_path = self.user_file_path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                loaded_users = pickle.load(file)
            for user in loaded_users:
                if self.username == user.username:
                    return False
            return True
        else:
            print('file doesnt exist yet')
            return True
        
    def save(self):
        """
        Validates username and saves user instance to users.pkl file. If username
        is already taken it is not saved and an error message is printed.

        If users.pkl doesn't exist then it is created and the specified user is saved.
        If it does exist the user is appended to the user list.
        """
        if self.validate_username():
            file_path = self.user_file_path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as read_file:
                    user_list = pickle.load(read_file)
                    user_list.append(self)

                with open(file_path, "wb") as write_file:
                    pickle.dump(user_list, write_file)
                return True
            else:
                new_user_list = [self]
                with open(file_path, "wb") as file:
                    pickle.dump(new_user_list, file)
                return True
        else:
            print(f"The username {self.username} is already taken")
            return False
            
    def get_user(self):
        """
        Matches username of the temp user with the actual user that is
        saved in the users file, if it exists. Returns actual user instance,
        or False. Used by auth_controller for authentication.
        """
        file_path = self.user_file_path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as read_file:
                user_list = pickle.load(read_file)
                for user in user_list:
                    if self.username == user.username:
                        return user
                return False
            
    def get_user_list(self):
        """
        Used by AuthController's update_user_settings to retrieve user
        list from user file.
        """
        file_path = self.user_file_path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as read_file:
                user_list = pickle.load(read_file)
                return user_list
            
    def save_user_list(self, user_list):
        """
        Used by AuthController's update_user_settings to save the
        updated user list to the user file.

        Parameters:
        user_list: list | list containing user objects
        """
        file_path = self.user_file_path
        if os.path.exists(file_path):
            with open(file_path, "wb") as file:
                pickle.dump(user_list, file)

    def set_program_directory(self):
        os_name = platform.system()
        if os_name == "Darwin":
            """
            Program files are stored in the following directories:
            MacOS: user/applications/Square Sync Manager
            Windows: ProgramFiles/Square Sync Manager
            """

            home_dir = str(Path.home())
            applications_dir = os.path.join(home_dir, "Applications")
            new_folder_name = "Square Sync Manager"
            new_folder_path = os.path.join(applications_dir, new_folder_name)
            

            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                self.program_directory = new_folder_path
                print(f"Folder '{new_folder_name}' created successfully in '{applications_dir}'.")
            else:
                print(f"Folder '{new_folder_name}' already exists in '{applications_dir}'.")
                self.program_directory = new_folder_path
            return new_folder_path

        elif os_name == "Windows":
            program_files_dir = os.environ["ProgramFiles"]
            new_folder_name = "Square Sync Manager"
            new_folder_path = os.path.join(program_files_dir, new_folder_name)

            if not os.path.exists(new_folder_path):
                try:
                    os.makedirs(new_folder_path)
                    print(f"Folder '{new_folder_name}' created successfully in '{program_files_dir}'.")
                except PermissionError:
                    print("Permission denied. Please run the script as an administrator.")
            else:
                print(f"Folder '{new_folder_name}' already exists in '{program_files_dir}'.")
            return new_folder_path

    def __str__(self):
        return f"{self.username}"
    
    def __repr__(self):
        return f"{self.username}"

class SecurePassword:
    """
    Takes users plain text password and saves it as a hash. Used in the User class.
    
    Attributes:
    secure_password: str | The hash of the users password

    Methods:
    password_hash(self, password):
        Hashes the plain-text password
    """
    def __init__(self, password: str):
        """
        Initialize SecurePassword object.

        Parameters:
        password: str | desired password
        """
        self.secure_password = self.password_hash(password)

    def password_hash(self, password: str):
        """
        Creates a hash of the users password and returns it.

        Parameters:
        password: str | desired password
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
                
    def __str__(self):
        return f"{self.secure_password}"