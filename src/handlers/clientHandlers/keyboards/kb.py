from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


back_to_client_interface = InlineKeyboardButton('Back to client menu⬅️', callback_data='start_as_client')
return_to_client_interface_kb = InlineKeyboardMarkup().add(back_to_client_interface)



search_by_id = InlineKeyboardButton('By id', callback_data='buy_by_id')

search_by_name = InlineKeyboardButton('By name', callback_data='buy_by_name')

buy_confirm = InlineKeyboardButton('Yes✅', callback_data='buy_confirm')

client_want_to_buy = InlineKeyboardMarkup().add(buy_confirm ,back_to_client_interface)

buy_option_id = InlineKeyboardMarkup().add(search_by_name,search_by_id)