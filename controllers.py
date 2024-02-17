from model_auth_user import *
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
class AuthController:
    def __init__(self):
        self.active_user = None
                    
    def login_user(self, username, password):
        '''
        Called by LoginView's login method upon login attempt. Creates a temp_user then calls the User models get_user method.
        If the get_user method returns a user instance then the temp_user and the matched_users passwords are compared. If
        successful the user is assigned as active and the instance is returned to the login view.
        '''
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
        '''
        Takes a user instance and password and checks if given password matches the
        instance's password hash.

        Note: The user instance cannot be a temp_user.
        '''
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == user.password:
            return True
        else:
            return False

    def update_user_settings_controller(self, argument_dict, active_user):
        '''
        Called by SettingsView's update_user_settings method.
        This function uses the argument dictionary to set the corresponding attributes of the
        active user using setattr(). User_list is then updated with the updated user.
        '''
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
        '''
        Creates a derived encryption key using the users password and the users
        randomly generated salt. Used in the encrypt and decrypt methods.
        '''
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
        '''
        Encrypts given data using the derived_key.
        '''
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data
    
    def decrypt(self, key, encrypted_data):
        '''
        Decrypts given encrypted data using the derived_key.
        '''
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data