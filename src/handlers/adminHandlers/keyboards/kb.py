from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


addProduct = InlineKeyboardButton('Add product📝', callback_data='admin_add')


completeCreatingProduct = InlineKeyboardButton('Complete✅', callback_data='admin_complete_creating')
cancelCreatingProduct = InlineKeyboardButton('Cancel❌', callback_data='admin_cancel')
back_to_admin_interface = InlineKeyboardButton('Back to admin menu⬅️', callback_data='start_as_admin')

admin_creating_product_kb = InlineKeyboardMarkup().add(completeCreatingProduct, cancelCreatingProduct)


deleteSearchByName = InlineKeyboardButton('By name', callback_data='delete_search_by_name')
deleteSearchById = InlineKeyboardButton('By ID', callback_data='delete_search_by_id')

delete_search_option = InlineKeyboardMarkup().add(deleteSearchByName, deleteSearchById)

changeSearchByName = InlineKeyboardButton('By name', callback_data='change_search_by_name')
changeSearchById = InlineKeyboardButton('By ID', callback_data='change_search_by_id')
startChanging = InlineKeyboardButton('Change', callback_data='start_changing')

completeChangingProduct = InlineKeyboardButton('Complete✅', callback_data='admin_change_creating')
cancelChangingProduct = InlineKeyboardButton('Cancel❌', callback_data='admin_cancel')

change_search_option = InlineKeyboardMarkup().add(changeSearchByName, changeSearchById)

change_create_keyboard = InlineKeyboardMarkup().add(back_to_admin_interface, addProduct)

change_or_leave_keyboard = InlineKeyboardMarkup().add(startChanging, back_to_admin_interface)

admin_changing_product_kb = InlineKeyboardMarkup().add(completeChangingProduct, cancelChangingProduct)

return_to_admin_interface_kb = InlineKeyboardMarkup().add(back_to_admin_interface)

empty_kb =InlineKeyboardMarkup()