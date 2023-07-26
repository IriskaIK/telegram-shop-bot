from aiogram import types
from aiogram.dispatcher import FSMContext

from models.session import dbController
from models.models import Product
from settings.bot_init import dp, bot
from .keyboards import kb
from ..state import Form




     
@dp.callback_query_handler(text = 'admin_add', state=[Form.admin_interface])
async def addProduct(callback_query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.product_name)
    
    

    await bot.send_message(callback_query.from_user.id, 'Enter product name:')

    await callback_query.answer()

@dp.message_handler(state=Form.product_name)
async def processProductName(message: types.Message, state: FSMContext):
    await state.set_state(Form.product_description)
    await state.update_data(product_name = message.text)
    await bot.send_message(message.from_user.id, 'Enter description:')

    
@dp.message_handler(state=Form.product_description)
async def processProductDesc(message: types.Message, state: FSMContext):
    await state.set_state(Form.product_price)
    await state.update_data(product_description = message.text)
    await bot.send_message(message.from_user.id, 'Enter price:')



@dp.message_handler(state=Form.product_price)
async def processProductPrice(message: types.Message, state: FSMContext):

    await state.set_state(Form.product_check)
    await state.update_data(product_price = message.text)
    
    pn = (await state.get_data('product_name')).get('product_name')
    pd = (await state.get_data('product_description')).get('product_description')
    pp = message.text
    
    await bot.send_message(message.from_user.id, f'Check your inputs:\nProduct name: {pn} \nDescription: {pd} \nPrice: {pp} UAH \n\nPress "Complete✅" if everything is ok. \nOtherwise press "Cancel❌"', reply_markup=kb.admin_creating_product_kb)


    
@dp.callback_query_handler(text = 'admin_complete_creating', state=Form.product_check)
async def processProduct(callback_query: types.CallbackQuery, state: FSMContext):
    pn = (await state.get_data('product_name')).get('product_name')
    pd = (await state.get_data('product_description')).get('product_description')
    pp = (await state.get_data('product_price')).get('product_price')
    
    session = dbController.get_session()

    with session() as s:
        product = Product(
            name= pn,
            description= pd,
            price= pp,
            isSelling = True
        )

        s.add(product)
        s.commit()
        await bot.send_message(callback_query.from_user.id, 'Succesfully created.\n'+ str(product), reply_markup=kb.return_to_admin_interface_kb)

    
   
    await callback_query.answer()




