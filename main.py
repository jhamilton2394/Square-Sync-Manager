import customtkinter
from views import *
from controllers import *

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

if __name__ == "__main__":
    controller = AuthController()
    app = App(controller)
    app.mainloop()