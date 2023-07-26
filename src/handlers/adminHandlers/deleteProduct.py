from aiogram import types
from aiogram.dispatcher import FSMContext

from models.session import dbController
from models.models import Product
from settings.bot_init import dp, bot
# from handlers.handlers import dp
from .keyboards import kb
from ..state import Form
from .service.ResponseGenerator import generateProductResponse


@dp.callback_query_handler(text = 'admin_remove', state=[Form.admin_interface])
async def askProductNameOrId(callback_query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.delete_search_by)
    

    await bot.send_message(callback_query.from_user.id, 'Search by name or by id?', reply_markup=kb.delete_search_option)

    await callback_query.answer()



@dp.callback_query_handler(text = 'delete_search_by_name', state=Form.delete_search_by)
async def AskProductName(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.delete_name)
    await bot.send_message(callback_query.from_user.id, 'Enter name of product to delete:')
    await callback_query.answer()

    
    
    
@dp.callback_query_handler(text = 'delete_search_by_id', state=Form.delete_search_by)
async def AskProductID(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.delete_id)
    await bot.send_message(callback_query.from_user.id, 'Enter id of product to delete:')

    await callback_query.answer()



@dp.message_handler(state=[Form.delete_name, Form.delete_id])
async def ProcessProductNameOrId(message: types.Message, state : FSMContext):
    curState = (await state.get_state())
    session = dbController.get_session()
    product = None
    with session() as s:
        if curState == 'Form:delete_name':
            product = s.query(Product).filter(Product.name == message.text).filter(Product.isSelling == True).all()
        elif curState == 'Form:delete_id':
            product = s.query(Product).filter(Product.id == message.text).all()
        
        if not product:
            await bot.send_message(message.from_user.id, 'Nothing with this name or Id. Try again:', reply_markup=kb.return_to_admin_interface_kb)
            return
        response = generateProductResponse(list(product))
        if len(list(product)) == 1:
            product[0].isSelling = False
            s.commit()
            await bot.send_message(message.from_user.id,f'Success!\n\n{response}Was deleted', reply_markup=kb.return_to_admin_interface_kb)
        else:
            await state.set_state(Form.delete_id)
            await bot.send_message(message.from_user.id, f'Multiple products found:\n{response}Enter id of product which you want to delete', reply_markup=kb.return_to_admin_interface_kb)
            
            return
        
    
    