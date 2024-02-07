from model_auth_user import *

class AuthController:
    # rename to auth_controller or 
    def __init__(self):
        self.active_user = None
            
    def auth_controller(self, username, password):
        '''
        Called by LoginView's authenticate method upon login attempt. Calls the User models login_user method.
        if the login_user method returns True then the active_user is set, and True
        is returned to the LoginView's authenticate method.
        '''
        user = User(username, password)
        if user.login_user():
            self.active_user = user.login_user()
            return True
        
    def login_user(self, username, password):
        temp_user = User(username, password)
        matched_user = temp_user.get_user()
        if matched_user:
            if matched_user.password == temp_user.password:
                self.active_user = matched_user
                return matched_user
            else:
                print(f"Incorrect password")
                print(f"the password you entered is {temp_user.password} of type {type(temp_user.password)}")
                return False
        else:
            print(f"no matched user")
            return False