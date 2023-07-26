from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


StartAdminBtn = InlineKeyboardButton('Start as admin🔑', callback_data='start_as_admin')
StartClientBtn = InlineKeyboardButton('Start as client🛒', callback_data='start_as_client')

start_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(StartAdminBtn, StartClientBtn)




addProduct = InlineKeyboardButton('Add product📝', callback_data='admin_add')
removeProduct = InlineKeyboardButton('Remove product🗑', callback_data='admin_remove')
changeProduct = InlineKeyboardButton('Change product🔧', callback_data='admin_change')
seeAllProducts = InlineKeyboardButton('See all products🔍', callback_data='admin_see')
SwitchToClient = InlineKeyboardButton('Switch to client🛒', callback_data='admin_switch_to_client')

admin_interface_kb = InlineKeyboardMarkup().row(addProduct, changeProduct).row(removeProduct, seeAllProducts).add(SwitchToClient)



clientAllProducts = InlineKeyboardButton('See all products🔍', callback_data='client_see')
ClientBuyProduct = InlineKeyboardButton('Buy product🛒', callback_data='client_buy')


client_interface_kb = InlineKeyboardMarkup().add(clientAllProducts, ClientBuyProduct)






