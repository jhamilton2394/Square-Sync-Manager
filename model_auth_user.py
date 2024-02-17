import hashlib
import pickle
import os

# Written by Jonathan Hamilton

"""
This module can act as a stand-alone authentication-user model. It contains tools for
creating users with secure passwords. Users are saved to the local machines file
system via pickling, but this can be easily modified to work with SQL and an ORM.
"""

class User:
    """
    Create a user with a username and password. Password is only saved as a hash.
    Refer to SecurePassword class for password details. The other instance variables
    are the user's inventory sheet header settings, as well as the salt, which is
    used for encryption of sensitive persistent data.
    """

    def __init__(self, username: str, password: str):
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

    def validate_username(self):
        """
        Checks if username already exists. Returns False if username exists, ie username is NOT valid.
        Returns True if username does not exist, ie username IS valid.

        Also checks if the file containing user data exists. If not, then no users yet exist and
        the function returns True.
        """
        file_path = 'files/users.pkl'
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
            file_path = 'files/users.pkl'
            if os.path.exists(file_path):
                with open(file_path, 'rb') as read_file:
                    user_list = pickle.load(read_file)
                    user_list.append(self)

                with open(file_path, "wb") as write_file:
                    pickle.dump(user_list, write_file)
            else:
                new_user_list = [self]
                with open(file_path, "wb") as file:
                    pickle.dump(new_user_list, file)
        else:
            print(f"The username {self.username} is already taken")
            
    def get_user(self):
        """
        Matches username of the temp user with the actual user that is
        saved in the users file, if it exists. Returns actual user instance,
        or False. Used by auth_controller for authentication.
        """
        file_path = 'files/users.pkl'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as read_file:
                user_list = pickle.load(read_file)
                for user in user_list:
                    if self.username == user.username:
                        return user
                return False
            
    def get_user_list(self):
        """
        Used by AuthController's update_user_settings_controller to retrieve user
        list from user file.
        """
        file_path = 'files/users.pkl'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as read_file:
                user_list = pickle.load(read_file)
                return user_list
            
    def save_user_list(self, user_list):
        """
        Used by AuthController's update_user_settings_controller to save the
        updated user list to the user file.
        """
        file_path = 'files/users.pkl'
        if os.path.exists(file_path):
            with open(file_path, "wb") as file:
                pickle.dump(user_list, file)

    def __str__(self):
        return f"{self.username}"
    
    def __repr__(self):
        return f"{self.username}"

class SecurePassword:
    """Takes users plain text password and saves it as a hash. Used in the User class."""
    def __init__(self, password: str):
        self.secure_password = self.password_hash(password)

    def password_hash(self, password: str):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
                
    def __str__(self):
        return f"{self.secure_password}"