import platform
import os
from pathlib import Path


"""
- Need a function that checks OS, then creates program directory in os specific location.
- Directory should then be saved somewhere so the program knows where to look for program files.
- Need to incorporate this path at every location that utilizes program files.
"""

"""
This function creates the program directory in the specified location depending
on the operating system.
"""

def set_program_directory():
    os_name = platform.system()
    if os_name == "Darwin":
        """
        Program files are stored in the following directories:
        MacOS: user/applications/Squarespace Companion
        Windows: ProgramFiles/Squarespace Companion
        """

        home_dir = str(Path.home())
        applications_dir = os.path.join(home_dir, "Applications")
        new_folder_name = "Squarespace Companion"
        new_folder_path = os.path.join(applications_dir, new_folder_name)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder '{new_folder_name}' created successfully in '{applications_dir}'.")
        else:
            print(f"Folder '{new_folder_name}' already exists in '{applications_dir}'.")
        return new_folder_path

    elif os_name == "Windows":
        program_files_dir = os.environ["ProgramFiles"]
        new_folder_name = "Squarespace Companion"
        new_folder_path = os.path.join(program_files_dir, new_folder_name)

        if not os.path.exists(new_folder_path):
            try:
                os.makedirs(new_folder_path)
                print(f"Folder '{new_folder_name}' created successfully in '{program_files_dir}'.")
            except PermissionError:
                print("Permission denied. Please run the script as an administrator.")
        else:
            print(f"Folder '{new_folder_name}' already exists in '{program_files_dir}'.")
        return new_folder_path