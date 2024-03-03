from controllers import *
from model_auth_user import *

controller = AuthController()

user = controller.login_user("carrot", "password")
key = controller.derive_key("password", user.salt)
dec_api_key = controller.decrypt(key, user.api_key)

user.api_key = dec_api_key

api = APIController(user)

#api.createAllProducts()

# value = api.pagesList()

# print(type(value))

print(api.getNumOfPages())
