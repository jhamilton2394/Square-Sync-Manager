# SquarespaceCompanion v0.0.1 is officially released as of March 28th 2023!
Squarespace Companion is an inventory manager for your Squarespace website. It automates the product upload process to save you time.
Additional functionalities are in development.

SquarespaceCompanion (from here on referred to as SSC) uses Squarespace's API and requires the Commerce Advanced subscription.

Here is a list of dependencies needed to run SSC:
Python 3.11
openpyxl 3.0.7
pandas 1.5.3
requests 2.28.2

NOTE: Excel is the only spreadsheet type supported in v0.0.1.

HOW IT WORKS:
Instead of creating products one at a time on your Squarespace website, SSC lets you import directly
from excel. This is especially useful if you use excel to track inventory.

After downloading and installing dependecies, then cloning the repository, a small amount of initial setup is required.
SSC needs a few pieces of information about your excel sheet in order to work, this information is referred to as the column
headers. SSC adapts to your spreadsheet so you don't have to change the layout for SSC to work properly. Simply tell it the 
names of the columns used for product name, sku, item description, price, and quantity. The column headers and the API key
will need to be setup in the 'settings' menu before creating any products from your inventory sheet.

Once your initial setup is done you can use your existing inventory excel spreadsheet to create batches of products,
or you can create individual products.

NOTE: Excel is the only spreadsheet type supported in v0.0.1. 
