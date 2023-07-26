from aiogram import types
from aiogram.dispatcher import FSMContext

from models.session import dbController
from models.models import Product
from settings.bot_init import dp, bot
from .keyboards import kb
from ..state import Form

from .service.ResponseGenerator import generateProductResponse



     
@dp.callback_query_handler(text = 'admin_change', state=[Form.admin_interface])
async def changeProduct(callback_query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.change_search_by)
    

    await bot.send_message(callback_query.from_user.id, 'Search by name or by id?', reply_markup=kb.change_search_option)

    await callback_query.answer()



@dp.callback_query_handler(text = 'change_search_by_name', state=Form.change_search_by)
async def AskProductName(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.change_name)
    await bot.send_message(callback_query.from_user.id, 'Enter name of product to change:')
    await callback_query.answer()

    
    
    
@dp.callback_query_handler(text = 'change_search_by_id', state=Form.change_search_by)
async def AskProductID(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.change_id)
    await bot.send_message(callback_query.from_user.id, 'Enter id of product to change:')

    await callback_query.answer()



@dp.message_handler(state=[Form.change_name, Form.change_id])
async def ProcessProductNameOrId(message: types.Message, state : FSMContext):
    curState = (await state.get_state())
    session = dbController.get_session()
    product = None
    with session() as s:
        if curState == 'Form:change_name':
            product = s.query(Product).filter(Product.name == message.text).filter(Product.isSelling == True).all()
        elif curState == 'Form:change_id':
            product = s.query(Product).filter(Product.id == message.text).all()
        
        if not product:
            await bot.send_message(message.from_user.id, 'Nothing with this name or Id. Enter name/id again or create new one', reply_markup=kb.change_create_keyboard)
            return
        response = generateProductResponse(list(product))
        if len(list(product)) == 1:
            await bot.send_message(message.from_user.id,f'Find!\n\n{response}Change it?', reply_markup=kb.change_or_leave_keyboard)
            await state.update_data(change_id = product[0].id)
        else:
            await state.set_state(Form.change_id)
            await bot.send_message(message.from_user.id, f'Multiple products found:\n{response}Enter id of product which you want to change', reply_markup=kb.return_to_admin_interface_kb)
            
            return
   
   
   
   
   
     
@dp.callback_query_handler(text = 'start_changing', state=[Form.change_name, Form.change_id])
async def changeProductName(callback_query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.product_change_name)
    
    

    await bot.send_message(callback_query.from_user.id, 'Enter new product name:')

    await callback_query.answer()

@dp.message_handler(state=Form.product_change_name)
async def processProductName(message: types.Message, state: FSMContext):
    await state.set_state(Form.product_change_description)
    await state.update_data(product_change_name = message.text)
    await bot.send_message(message.from_user.id, 'Enter new description:')

    
@dp.message_handler(state=Form.product_change_description)
async def processProductDesc(message: types.Message, state: FSMContext):
    await state.set_state(Form.product_change_price)
    await state.update_data(product_change_description = message.text)
    await bot.send_message(message.from_user.id, 'Enter new price:')



@dp.message_handler(state=Form.product_change_price)
async def processProductPrice(message: types.Message, state: FSMContext):

    await state.set_state(Form.product_change_check)
    await state.update_data(product_change_price = message.text)
    
    pn = (await state.get_data('product_change_name')).get('product_change_name')
    pd = (await state.get_data('product_change_description')).get('product_change_description')
    pp = message.text
    
    await bot.send_message(message.from_user.id, f'Check your inputs:\nProduct name: {pn} \nDescription: {pd} \nPrice: {pp} UAH \n\nPress "Complete✅" if everything is ok. \nOtherwise press "Cancel❌"', reply_markup=kb.admin_changing_product_kb)


    
@dp.callback_query_handler(text = 'admin_change_creating', state=Form.product_change_check)
async def processProduct(callback_query: types.CallbackQuery, state: FSMContext):
    pn = (await state.get_data('product_change_name')).get('product_change_name')
    pd = (await state.get_data('product_change_description')).get('product_change_description')
    pp = (await state.get_data('product_change_price')).get('product_change_price')
     
    pi = (await state.get_data('change_id')).get('change_id')
    session = dbController.get_session()

    with session() as s:
        product = s.query(Product).filter(Product.id == pi).first()
        product.name = pn
        product.description = pd
        product.price = pp
        s.commit()
        await bot.send_message(callback_query.from_user.id, 'Succesfully changed.\n'+ str(product), reply_markup=kb.return_to_admin_interface_kb)

    
   
    await callback_query.answer()
 
    

# session = dbController.get_session()

# with session() as s:
#     user = User(
#         tg_id = 2,
#         username = 'spongebob'
#     )

#     s.add(user)
#     s.commit()