# SquarespaceCompanion
Squarespace Companion is an inventory manager for your Squarespace website. It automates the product upload process to save you time.
Additional functionalities are in development.

SquarespaceCompanion uses Squarespace's API.

Version 0.0.0 is still in development, but is expected to be usable by the end of March 2023.

Here is a list of dependencies needed to run Squarespace companion:
Python 3.11
openpyxl 3.0.7
pandas 1.5.3
requests 2.28.2
numbers_parser 3.9.5 if using .numbers files on Mac **


IMPORTANT
For all functions to work properly you must create a file called "keys.py" with a variable named "apiKey" set equal to your
Squarespace api key. This file should be included in the .gitignore file to prevent exposing your key.

** (numbers parser requires python-snappy, which needs snappy installed from homebrew first. Example on Mac:
'brew install snappy' then 'pip3 install numbers-parser' if the install fails then 'pip3 install python-snappy'
then retry the numbers parser install.)
