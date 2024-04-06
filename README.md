# Square Sync Manager v0.0.3.1 is officially released as of January 21st 2024!
Square Sync Manager is an inventory manager for your Squarespace ecommerce website. It automates the product upload process to save you time.
Additional functionalities are in development.

Square Sync Manager (from here on referred to as SSM) uses Squarespace's API and requires the Commerce Advanced subscription.

NOTE: Excel is the only spreadsheet type supported in v0.0.1 through v0.0.3.1 (current version)

HOW IT WORKS:
Instead of creating products one at a time on your Squarespace website, SSM lets you import directly
from excel. This is especially useful if you use excel to track inventory.

After downloading and installing the most recent release, a small amount of initial setup is required.
SSM needs a few pieces of information about your excel sheet in order to work, this information is referred to as the column
headers. SSM adapts to your spreadsheet so you don't have to change the layout for SSM to work properly. Simply tell it the 
names of the columns used for product name, sku, item description, price, and quantity (a 'Deleted' column was added in v0.0.3. See update notes).
The column headers and the API key will need to be setup in the 'settings' menu before creating any products from your inventory sheet.

Once your initial setup is done you can use your existing inventory excel spreadsheet to create batches of products.

-Check out the Squarespace Account tutorial here if you don't have a squarespace website but would like to try out our app.
-Check out the Square Sync Manager tutorial here if you'd like more in depth instructions.
-If you're an evaluator that is here to check out my coding skills, please go check out the project resume here.

v0.0.3 fixes the duplicate product problem when creating new products. When creating a batch of products from your working inventory,
SSM will now compare site inventory against your working inventory, and only create the products that are not already on the site.
For products that have been deleted from the site that you do not wish to have created again, you must create a new column in your
spreadsheet, name it 'Deleted' or something similar, then configure your column header in settings. Any product with an 'x' in this
column will be 'marked as deleted by user' and will not be created.

v0.0.3.1 includes dependency updates and bug fixes.
