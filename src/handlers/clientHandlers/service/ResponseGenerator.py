def generateClientProductResponse(list_of_products):
    response = ''
    for i in range(len(list(list_of_products))):
        response += f'Name: {list_of_products[i].name}\nDesription: {list_of_products[i].description}\nPrice: {list_of_products[i].price} UAH\nID: {list_of_products[i].id}' 
        response += '\n\n'
        
    return response