### functions used for square and weebly, derived from squarespace companion
import requests
import json
from pandas import ExcelFile
import weeblyKeys as wk
import uuid


### first product query seems to work. returns nothing but a 200 so far, need to add more products.
def weeblyProductQuery(prodID):
    baseURL = 'https://connect.squareup.com/v2/inventory/'
    endURL = '?location_ids='
    completeURL = (baseURL + str(prodID) + endURL)
    prodHeaders = {'Square-Version': '2023-03-15',
                'Authorization': 'Bearer ' + wk.apiKey,
               'Content-Type': 'application/json'}
    r = requests.get(completeURL, headers=prodHeaders)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return
    
def idempotencyKey():
    key = uuid.uuid4()
    return key


### Using squarespace product creation as framework, we are going to build the weebly product creation.
#   Adapted URL and headers, as well as a basic product info in the dataoutbox.
def weeblyCreateProduct(sku, name, description, price, qty):
    id = name.replace(" ", "")
    id2 = id + '2'
    dataOutbox = {"idempotency_key": str(idempotencyKey()),
                    "object": {"id": "#" + id,
                                "type": "ITEM",
                                "item_data": {"name": name,
                                                "description": description,
                                                "variations": [{"id": "#" + id2,
                                                                "type": "ITEM_VARIATION",
                                                                "item_variation_data": {
                                                                                        "price_money": {
                                                                                                        "amount": price,
                                                                                                        "currency": "USD"
                                                                                                        },
                                                                                                        "pricing_type": "FIXED_PRICING",
                                                                                                        "sku": sku
                                                                                        },
                                                                "product_set_data": {"quantity_exact": qty}
                                                        }]
                                                }
                                 }
                 }
    
    jsonDataOutbox = json.dumps(dataOutbox)
    prodURL = 'https://connect.squareup.com/v2/catalog/object'
    prodHeaders = {'Square-Version': '2023-04-19',
                'Authorization': 'Bearer ' + wk.apiKey,
               'Content-Type': 'application/json'}
    r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return

weeblyCreateProduct(sku='1231', name='cafe mocha', description='delicious chocolaty coffee', price=400, qty=17)

def weeblyCreateAllProducts(file, id):
    #opening column header files for input into loop
    sku1 = open('skufile.txt', 'r')
    skuHeader = (sku1.read())
    name1 = open('namefile.txt', 'r')
    nameHeader = (name1.read())
    
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



#first error
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "MISSING_REQUIRED_PARAMETER",
         "detail": "Field must be set",
         "field": "object"
      }
   ]
}

#second error
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "EXPECTED_OBJECT",
         "detail": "Expected an object value.",
         "field": "object"
      }
   ]
}

#third error, finally getting somewhre
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "BAD_REQUEST",
         "detail": "Item with name Tea and token #Tea must have at least one variation."
      }
   ]
}
#added variation

#fourth error
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "EXPECTED_ARRAY",
         "detail": "Expected an array.",
         "field": "object.item_data.variations"
      }
   ]
}
#had deleted the list brackets immediately after "variations", re-added them.

#fifth error
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "INVALID_VALUE",
         "detail": "Object `#Tea` of type ITEM references unknown object #Beverages in attr SQ_COGS_MCID"
      }
   ]
}

#deleted the whole #beverages line

#6th error
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "IDEMPOTENCY_KEY_REUSED",
         "detail": "The idempotency key can only be retried with the same request data.",
         "field": "idempotency_key"
      }
   ]
}

#changed last two digits of key

#7th error
#<Response [400]>
{
   "errors": [
      {
         "category": "INVALID_REQUEST_ERROR",
         "code": "INVALID_VALUE",
         "detail": "Object `#42RCVEOEG6Q4QQRCGB5KOU63` of type ITEM_FEE_MEMBERSHIP references unknown object #SalesTax in attr SQ_COGS_FID"
      }
   ]
}

#deleted out sales tax line

#8th try is the charm!! Success!
#<Response [200]>
# {
#    "catalog_object": {
#       "type": "ITEM",
#       "id": "7FVH436DLPFC42WGIG6VFT7Q",
#       "updated_at": "2023-04-21T01:55:16.473Z",
#       "created_at": "2023-04-21T01:55:16.473Z",
#       "version": 1682042116473,
#       "is_deleted": false,
#       "present_at_all_locations": true,
#       "item_data": {
#          "name": "Tea",
#          "description": "Hot Leaf Juice",
#          "is_taxable": true,
#          "variations": [
#             {
#                "type": "ITEM_VARIATION",
#                "id": "V4ZAX2PGNRWYPHBVF4NQHTZO",
#                "updated_at": "2023-04-21T01:55:16.473Z",
#                "created_at": "2023-04-21T01:55:16.473Z",
#                "version": 1682042116473,
#                "is_deleted": false,
#                "present_at_all_locations": true,
#                "item_variation_data": {
#                   "item_id": "7FVH436DLPFC42WGIG6VFT7Q",
#                   "name": "Green Tea",
#                   "ordinal": 0,
#                   "pricing_type": "FIXED_PRICING",
#                   "price_money": {
#                      "amount": 150,
#                      "currency": "USD"
#                   },
#                   "sellable": true,
#                   "stockable": true
#                }
#             }
#          ],
#          "product_type": "REGULAR",
#          "description_html": "<p>Hot Leaf Juice</p>",
#          "description_plaintext": "Hot Leaf Juice"
#       }
#    },
#    "id_mappings": [
#       {
#          "client_object_id": "#Tea",
#          "object_id": "7FVH436DLPFC42WGIG6VFT7Q"
#       },
#       {
#          "client_object_id": "#teaapparently",
#          "object_id": "V4ZAX2PGNRWYPHBVF4NQHTZO"
#       }
#    ]
# }