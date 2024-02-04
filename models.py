import hashlib
import pickle
import os

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

    def __str__(self):
        return f"{self.username}"
    
    def __repr__(self):
        return f"{self.username}"
        
    '''
    save user function:
    check if file even exists:
    if yes then:
    
    open file
    unpickle the user list
    append new user
    pickle the appended list

    if not:
    open and create user file
    create user list with new user
    pickle it

    should probably have a validate function that makes sure user doesn't already exist
    '''


class SecurePassword:
    '''
    Takes users typed password and saves it as a hash. Used in the User class.
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
    
new_user = User("biscuitbuns23", "Jamnjerk747!!")

new_user2 = User("chubs", "password")

user_list = []

user_list.append(new_user)
user_list.append(new_user2)


with open('files/users.pkl', 'wb') as file:
    pickle.dump(user_list, file)
print("pickled the list")

with open('files/users.pkl', 'rb') as file:
    loaded_objects = pickle.load(file)
print(type(loaded_objects))
    
# for objects in loaded_objects:
#     print(object.username)

new_user3 = User("babyCakes", "password2")

new_user4 = User("crabby baby", "password2")


print(new_user4.validate_username())