from controllers import *
from model_auth_user import *

"""
Sets up Auth controller and authenticated user in order to test the
api controller.
"""

controller = AuthController()

new_user = User("carrot", "password")
new_user.save()

user = controller.login_user("gook", "password")
key = controller.derive_key("password", user.salt)
dec_api_key = controller.decrypt(key, user.api_key)
user.api_key = dec_api_key

api = APIController(user)
api.set_store_pages_info()