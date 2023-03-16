###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts as cp
import json
import keys as k
import requests
import pandas


###CURRENTLY WORKING ON RETREIVING PAGE ID FOR USE IN PRODUCT CREATION
###get pages, gets page ID's
def getPages():
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    getStorePagesHeaders = {'Authorization': 'Bearer ' + k.apiKey,
                            'User-Agent': 'APIAPP1.0'}
    r = requests.get(getStorePagesURL, headers=getStorePagesHeaders)
    data = r.json()
    df = pandas.DataFrame(r)
    print(data)

getPages()