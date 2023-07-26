from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup



class Form(StatesGroup):

    default = State()  
    user = State()
    last_message_id = State()
    
    admin_interface = State()
    
    
    product_name = State()
    product_description = State()
    product_price = State()
    product_check = State()
    
 
    delete_search_by=State()
    delete_name = State()
    delete_id = State()
    
    
    change_search_by= State()
    change_name = State()
    change_id = State()
    
    product_change_name = State()
    product_change_description=State()
    product_change_price = State()
    product_change_check =State()
    
    
    see_all_products = State()
    buy_search_by = State()
    buy_name = State()
    buy_id = State()
    id_of_product = State()
    client_interface = State()
    




