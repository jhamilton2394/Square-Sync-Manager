1. If you don't have a Squarespace website set up, follow my Squarespace account setup tutorial [here](https://github.com/biscuitbuns23/Square-Sync-Manager/blob/Initial-consolidated/docs/Squarespace%20account%20tutorial.md) (It's in the docs folder).
   
2. Follow the instructions for downloading and installing the latest release [here](https://github.com/biscuitbuns23/Square-Sync-Manager/releases).
   
3. Open Square Sync Manager, create your account, and proceed to the settings page.
The entry fields on the settings page each correspond to a column header on your inventory
file. In order to upload the items to your website SSM needs to know exactly what these column
headers are called so it can assemble the product information correctly. Fill in all the entry
fields using the image below as a reference. There is a special column called "Deleted" that you must include. This column dictates
whether or not the item will be excluded from the upload process. If there are products
that have already sold out, or have been taken down, then simply mark this column with an
x and it will be excluded. (Also note that duplicate items will NOT be created if you
upload the same sheet more than once. Every item is checked against the current inventory
on the website to ensure no duplicates are created.)

<img width="1679" alt="Settings config example" src="https://github.com/biscuitbuns23/Square-Sync-Manager/assets/28676599/c4ca414b-1427-4a88-831f-10321abba5ad">

5. Next you need to enter your API key in the corresponding field. The Squarespace account setup
instructions in step 1 will tell you where to find the API key.

6. You'll need to select your inventory file. If you don't have one yet you can use
the inventory template included under the "docs" folder.

7. Now you're ready to upload the items from your inventory sheet to your website.
Navigate to the Create Products tab and select the store page you'd like to
upload to, Then click upload to site.
<img width="1147" alt="create products" src="https://github.com/biscuitbuns23/Square-Sync-Manager/assets/28676599/cdb88b72-83b8-4b9e-b09c-afede0200278">

```
It may take some time to upload depending on the number of products you have. You'll see a loading wheel
until the upload process finishes. Once it's complete the details will be displayed in the terminal.
```
