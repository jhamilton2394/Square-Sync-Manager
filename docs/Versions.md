v1.0.0 Implements secure authentication system as well as a new user interface.

v0.0.3.1 includes dependency updates and bug fixes.

v0.0.3 fixes the duplicate product problem when creating new products. When creating a batch of products from your working inventory,
SSM will now compare site inventory against your working inventory, and only create the products that are not already on the site.
For products that have been deleted from the site that you do not wish to have created again, you must create a new column in your
spreadsheet, name it 'Deleted' or something similar, then configure your column header in settings. Any product with an 'x' in this
column will be 'marked as deleted by user' and will not be created.
