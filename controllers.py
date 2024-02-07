from model_auth_user import *

class AuthController:
    def __init__(self):
        self.active_user = None
            
    def auth_controller(self, username, password):
        '''
        Called by LoginView's login method upon login attempt. Creates a temp_user then calls the User models get_user method.
        If the get_user method returns a user instance then the temp_user and the matched_users passwords are compared. If
        successful the user is assigned as active and the instance is returned to the login view.
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
                return False
        else:
            return False