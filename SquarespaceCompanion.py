###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts

x  = input('would you like to run the function?')
if x == 'yes':
    createProducts.createProduct(storePageID='6404283498e5bf333e47441a',
                                productName='Posies',
                               productDescription='<p> some posies </p>',
                              variantSku='8008s', productPrice='100')
