import tkinter as tk
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Squarespace Companion")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Menu logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="Menu",
                                                 font=customtkinter.CTkFont(size=30,
                                                                            weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,10))
        
        # Create products button
        self.create_prod_button = customtkinter.CTkButton(self.sidebar_frame, text="Create Products", width = 140)
        self.create_prod_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Settings button
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", width = 140)
        self.settings_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # info button
        self.info_button = customtkinter.CTkButton(self.sidebar_frame, text="Info", width = 140)
        self.info_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # create second sidebar frame for practice
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=200, corner_radius=2)
        self.sidebar_frame2.grid(row=0, column=2, rowspan=4, padx=40,  sticky="nsew")
        self.input_button = customtkinter.CTkButton(self.sidebar_frame2, text="click for input", command=self.input_dialog_event)
        self.input_button.grid(row=0, column=0, padx=20, pady=10)

        # create textbox
        # self.textbox = customtkinter.CTkTextbox(self, width=250)
        # self.textbox.grid(row=0, column=1, padx=20, pady=20)

        # create text
        self.announcement_box = tk.Text(self, wrap="word", width=250)
        self.announcement_box.insert("1.0",
                                     '''Welcome to Squarespace Companion!

If you have not already, please configure your settings
under the settings option in the main menu.''')
        self.announcement_box.config(state="disabled", font="Helvetica")
        self.announcement_box.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")


        # create entry
        # self.entry = customtkinter.CTkEntry(self.sidebar_frame, width=150)
        # self.entry.grid(row=1, column=0, padx=(20, 2), pady=20)

        # self.entry.bind("<Return>", command=self.submit_button_event)
        
        # create entry submit button
        # self.submit_button = customtkinter.CTkButton(self.sidebar_frame, text="Submit", command=self.submit_button_event, width=50)
        # self.submit_button.grid(row=1, column=1, padx=(2, 10), pady=20)







        # Load image
        # image_path = "mars_pic.jpeg"
        # self.image = Image.open(image_path)

        #resize the image
        # width, height = self.image.size
        # new_width = int(width * 2)
        # new_height = int(height * 2)
        # self.resized_image = self.image.resize((new_width, new_height))

        # Convert the image to customkinter PhotoImage
        #self.photo = ImageTk.PhotoImage(self.image)
        # 237 x 148 original. x5 = 1185 x 740
        # self.photo1 = customtkinter.CTkImage(self.image, size=(237, 148))

        # Create a Label widget to display the image
        # self.label1 = customtkinter.CTkLabel(self.sidebar_frame, image=self.photo1, text=None, width=240, corner_radius=30)
        # self.label1.grid(row=2, column=0, columnspan=2)








    def input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="input here", title="dialog box")
        print(dialog.get_input())

    def submit_button_event(self, event=None):
        input = self.entry.get()
        self.entry.delete(0, 100)
        if input == '':
            None
        else:
            print(input)
       

if __name__ == "__main__":
    app = App()
    app.mainloop()