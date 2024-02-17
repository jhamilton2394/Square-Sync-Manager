import customtkinter
from views import *
from controllers import *

'''
Dear evaluators,

This app follows the MVC architecture. Refer to the applicable models, views, or controller files as needed.

All data is stored in files under the files folder using Pickle. The apps small size and intended user base
does not warrant the use of SQL. All sensitive data is either hashed or encrypted before being stored.
'''

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

if __name__ == "__main__":
    auth_controller = AuthController()
    app = App(auth_controller)
    app.mainloop()