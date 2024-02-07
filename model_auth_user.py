import hashlib
import pickle
import os

# Written by Jonathan Hamilton

'''
This module can act as a stand-alone authentication-user model. It contains tools for
creating users with secure passwords. Users are saved to the local machines file
system via pickling, but this can be easily modified to work with SQL and an ORM.
'''

class User:
    '''
    Create a user with a username and password. Password is only saved as a hash.
    Refer to SecurePassword class for password details.
    '''
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = str(SecurePassword(password))

    def validate_username(self):
        '''
        Checks if username already exists. Returns False if username exists, ie username is NOT valid.
        Returns True if username does not exist, ie username IS valid.

        Also checks if the file containing user data exists. If not, then no users yet exist and
        the function returns True.
        '''
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
        '''
        Validates username and saves user instance to users.pkl file. If username
        is already taken it is not saved and an error message is printed.

        If users.pkl doesn't exist then it is created and the specified user is saved.
        If it does exist the user is appended to the user list.
        '''
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
        '''
        Matches username of the temp user with the actual user that is
        saved in the users file, if it exists. Returns actual user instance.
        Used by auth_controller for authentication.
        '''
        file_path = 'files/users.pkl'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as read_file:
                user_list = pickle.load(read_file)
                for user in user_list:
                    if self.username == user.username:
                        return user
                return False

    def __str__(self):
        return f"{self.username}"
    
    def __repr__(self):
        return f"{self.username}"

class SecurePassword:
    '''
    Takes users plain text password and saves it as a hash. Used in the User class.
    '''
    def __init__(self, password: str):
        self.secure_password = self.password_hash(password)

    def password_hash(self, password: str):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def validate_password(user, password: str):
        '''
        Takes a user instance and password and checks if given password matches the
        instance's password hash.
        '''
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == user.password:
            return True
        else:
            return False
            
    def __str__(self):
        return f"{self.secure_password}"
    

'''
-create a retreive user method that returns the requested
 user instance DONE
-delegate "validate user" to the auth controller.
-delegate the "validate password" method to auth controller
 auth cont will need to receive a user instance
'''