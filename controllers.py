from model_auth_user import *

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
        Parameters:
            argument_dict (dict): Contains the settings to be updated.
            active_user (User): The active user whose settings will be updated.

        Returns:
            User: The updated active user.

        This function uses the argument dictionary to set the corresponding attributes of the
        active user using setattr().

        Additionally, it updates the user list with the updated user info, then calls
        save_user_list() to save it.

        Example usage:
            argument_dict = {'username': 'new_username', 'api_key': '34jAS$##Fddu3!@SSdfvdDD#'}
            updated_user = update_user_settings_controller(argument_dict, active_user)
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
