import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = SecurePassword(password)

    def __str__(self):
        return f"{self.username}"

class SecurePassword:
    def __init__(self, password):
        self.secure_password = self.password_hash(password)

    def password_hash(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    def check_password(user, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == user.password:
            return True
        else:
            return False

    
    def __str__(self):
        return f"{self.secure_password}"
    
new_user = User("biscuitbuns23", "Jamnjerk747!!")

print(SecurePassword.check_password(new_user, "Jamnjerk747!!"))

