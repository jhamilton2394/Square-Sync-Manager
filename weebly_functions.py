### functions used for square and weebly, derived from squarespace companion
import requests
import json
from pandas import ExcelFile

### first product query seems to work. returns nothing but a 200 so far, need to add more products.
def weeblyProductQuery(prodID):
    baseURL = 'https://connect.squareup.com/v2/inventory/'
    endURL = '?location_ids='
    completeURL = (baseURL + str(prodID) + endURL)
    prodHeaders = {'Square-Version': '2023-03-15',
                'Authorization': 'Bearer EAAAF_9v3aCUH9u4OGZk5EGEsLngPKx295Y3skQWfIP2xpIleS6kt3_oKfnctwy5',
               'Content-Type': 'application/json'}
    r = requests.get(completeURL, headers=prodHeaders)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return
    
weeblyProductQuery(666)

### Using squarespace product creation as framework, we are going to build the weebly product creation.
def weeblyCreateProduct(storePageID, productName, productDescription, variantSku, productPrice, quantity):
    dataOutbox = {"idempotency_key": "789ff020-f723-43a9-b4b5-43b5dc1fa3dc",
                    "batches": [{"objects": [{"type": "ITEM",
                                                "id": "#Tea",
                                                "present_at_all_locations": True,
                                                "item_data": {"name": "Tea",
                                                                "description": "Hot Leaf Juice",
                                                                "category_id": "#Beverages",
                                                                "tax_ids": ["#SalesTax"]
                                                             }
                                            }]
                                }]
                }
    jsonDataOutbox = json.dumps(dataOutbox)
    prodURL = 'https://connect.squareup.com/v2/catalog/batch-upsert'
    prodHeaders = {'Square-Version': '2023-03-15',
                'Authorization': 'Bearer ' + retreiveApiKey(),
               'Content-Type': 'application/json'}
    r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return



def weeblyCreateAllProducts(file, id):
    #opening column header files for input into loop
    name1 = open('namefile.txt', 'r')
    nameHeader = (name1.read())
    sku1 = open('skufile.txt', 'r')
    skuHeader = (sku1.read())
    item_desc1 = open('item_desc_file.txt', 'r')
    item_desc_header = (item_desc1.read())
    price1 = open('pricefile.txt', 'r')
    priceHeader = (price1.read())
    qty1 = open('qtyfile.txt', 'r')
    qtyHeader = (qty1.read())
    del1 = open('delfile.txt', 'r')
    delHeader = (del1.read())
    #open excel doc
    xls = ExcelFile(file)
    df = xls.parse(xls.sheet_names[0])
    product_list = site_master_prod_list()
    #loop thru doc & create products using column header files.
    for i in range(len(df)):
        sku = str((df.loc[i].at[skuHeader]))
        name = (df.loc[i].at[nameHeader])
        itemDesc = (df.loc[i].at[item_desc_header])
        price = str((df.loc[i].at[priceHeader]))
        quant = str((df.loc[i].at[qtyHeader]))
        del2 = (df.loc[i].at[delHeader])
        pageID = id
        if name in product_list:
            print(name, 'already on site, skipping...\n')
        elif del2 == 'x':
            print(name, 'previously deleted from site by user, skipping...')
        else:
            weeblyCreateProduct(storePageID=pageID,
                            productName=name,
                        productDescription=itemDesc,
                        variantSku=sku,
                        productPrice=price,
                        quantity=quant)


### square batch product creation template
'''   
curl https://connect.squareup.com/v2/catalog/batch-upsert \
  -X POST \
  -H 'Square-Version: 2023-03-15' \
  -H 'Authorization: Bearer ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"idempotency_key": "789ff020-f723-43a9-b4b5-43b5dc1fa3dc",
        "batches": [{"objects": [{"type": "ITEM",
                                "id": "#Tea",
                                "present_at_all_locations": true,
                                "item_data": {"name": "Tea",
                                                "description": "Hot Leaf Juice",
                                                "category_id": "#Beverages",
                                                "tax_ids": ["#SalesTax"]
                                                }
                            }]
                }]
        }'
'''

### This is only an example. The weebly data returned from a request will likely be vastly different.
# def site_master_prod_list():
#     #Initial product query
#     actual_prod_list = []
#     ###Commenting out 2 lines below, which just opens the data file. The file was used for testing purposes.
#     # open_product_data = open('product_file', 'r')
#     # raw_data = open_product_data.read()
#     raw_data = getProducts()
#     prod_main_dict = json.loads(raw_data)
#     prod_list = prod_main_dict['products']
#     pagination = prod_main_dict['pagination']
#     cursor = pagination['nextPageCursor']
#     for i in prod_list:
#         actual_prod_list.append(i['name'])
#     ###Loops through all pages if they exist.
#     while pagination['hasNextPage'] == True:
#         raw_data = getProducts(cursor)
#         prod_main_dict = json.loads(raw_data)
#         prod_list = prod_main_dict['products']
#         pagination = prod_main_dict['pagination']
#         cursor = pagination['nextPageCursor']
#         for i in prod_list:
#             actual_prod_list.append(i['name'])
#     return actual_prod_list
