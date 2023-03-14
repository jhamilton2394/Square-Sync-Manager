import requests
import json
from pandas import ExcelFile

### Import excel file containing inventory to be loaded to squarespace.
xls = ExcelFile('C:/Users/Hamiltons/Jonathan/Python Programs/dress inventory.xlsx')

df = xls.parse(xls.sheet_names[0])

### Defining our function to create new products
def createProduct(storePageID, productName, productDescription, variantSku, productPrice):
    '''
    storePageID = '6404283498e5bf333e47441a'
    productName = 'Pussy bowl'
    productDescription = '<p> A half dozen assorted Pussies. MMMMMM </p>'
    variantSku = 'XB55555'
    productPrice = '10'
    '''
    dataOutbox = {'type': 'PHYSICAL',
              'storePageId': storePageID,
               'name': productName,
               'description': productDescription,
               'isVisible': 'true',
               'variants': [{'sku': variantSku,
                            'pricing': {'basePrice': {'currency': 'USD',
                                                      'value': productPrice
                                                      }
                                        }
                             }
                            ]
                }

    jsonDataOutbox = json.dumps(dataOutbox)
    prodURL = 'https://api.squarespace.com/1.0/commerce/products'
    prodHeaders = {'Authorization': 'yourAPIKEY',
               'User-Agent': 'APIAPP1.0',
               'Content-Type': 'application/json'}
    r = requests.post(prodURL, headers=prodHeaders, data = jsonDataOutbox)
    json_data = r.json()
    pretty_json_data = json.dumps(json_data, indent=3)
    print(r)
    print(pretty_json_data)
    return


