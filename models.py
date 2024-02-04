import hashlib

class User:
    '''
    Create a user with a username and password. Password is only saved as a hash.
    Refer to SecurePassword class for password details.
    '''
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = str(SecurePassword(password))

    def __str__(self):
        return f"{self.username}"

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

result = SecurePassword.validate_password(new_user, "Jamnjerk747!!")

print(result)

#print(new_user.password)