def generateProductResponse(list_of_products):
    response = ''
    for i in list_of_products:
        response += str(i) 
        response += '\n\n'
        
    return response