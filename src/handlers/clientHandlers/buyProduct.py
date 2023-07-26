from aiogram import types
from aiogram.dispatcher import FSMContext

from models.session import dbController
from models.models import Product, User, Order
from settings.bot_init import dp, bot
# from handlers.handlers import dp
from .keyboards import kb
from ..state import Form
from .service.ResponseGenerator import generateClientProductResponse
from aiogram.types.message import ContentType

from dotenv import load_dotenv
import os

@dp.callback_query_handler(text = 'client_buy', state=[Form.client_interface])
async def askProductNameOrId(callback_query: types.CallbackQuery, state: FSMContext):

    await state.set_state(Form.buy_search_by)
    

    await bot.send_message(callback_query.from_user.id, 'Search by name or by id?', reply_markup=kb.buy_option_id)

    await callback_query.answer()



@dp.callback_query_handler(text = 'buy_by_name', state=Form.buy_search_by)
async def AskProductName(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.buy_name)
    await bot.send_message(callback_query.from_user.id, 'Enter name of product:')
    await callback_query.answer()

    
    
    
@dp.callback_query_handler(text = 'buy_by_id', state=Form.buy_search_by)
async def AskProductID(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.buy_id)
    await bot.send_message(callback_query.from_user.id, 'Enter id of product:')

    await callback_query.answer()



@dp.message_handler(state=[Form.buy_name, Form.buy_id])
async def ProcessProductNameOrId(message: types.Message, state : FSMContext):
    curState = (await state.get_state())
    session = dbController.get_session()
    product = None
    with session() as s:
        if curState == 'Form:buy_name':
            product = s.query(Product).filter(Product.name == message.text).filter(Product.isSelling == True).all()
        elif curState == 'Form:buy_id':
            product = s.query(Product).filter(Product.id == message.text).all()
        
        if not product:
            await bot.send_message(message.from_user.id, 'Nothing with this name or Id. Try again:', reply_markup=kb.return_to_client_interface_kb)
            return
        response = generateClientProductResponse(product)
        if len(list(product)) == 1:
            #ask if he really want to buy it
            await state.update_data(id_of_product = int(product[0].id))
            product_id = (await state.get_data('id_of_product')).get('id_of_product')
            await bot.send_message(message.from_user.id,f'Find!\n\n{response}\n\n Do you want to buy it?', reply_markup=kb.client_want_to_buy)
        else:
            await state.set_state(Form.buy_id)
            await bot.send_message(message.from_user.id, f'Multiple products found:\n{response}Enter id of product which you want', reply_markup=kb.return_to_client_interface_kb)
            
            return
        
    
    
@dp.callback_query_handler(text = 'buy_confirm', state=[Form.buy_name, Form.buy_id])
async def BuyProductInvoice(callback_query: types.CallbackQuery, state: FSMContext):
    load_dotenv()
    
    invoice_token = os.environ.get('payment_token')
    product_id = (await state.get_data('id_of_product')).get('id_of_product')
    session = dbController.get_session()
    with session() as s:
        product = s.query(Product).filter(Product.id == product_id).all()
        
        PRICE = types.LabeledPrice(label=product[0].name, amount= int(float(product[0].price)*100))
    print(1)
    await bot.send_invoice(callback_query.from_user.id, 
                           title=product[0].name, 
                           description=product[0].description, 
                           payload=product[0].id, 
                           provider_token=invoice_token,
                           currency='UAH', 
                           prices=[PRICE])
    print(1)
    await callback_query.answer()

@dp.pre_checkout_query_handler(lambda query: True, state='*')
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    print(1)
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment.to_python()

    product_id = payment_info['invoice_payload']
    session = dbController.get_session()
    with session() as s:
        product = s.query(Product).filter(Product.id == product_id).first()
        user = s.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        order = Order(product = product, owner = user)
        s.add(order)
        s.commit()
    await bot.send_message(message.chat.id, f"Success! You have bought something. This info have been saved in database.\n\nThank you for testing how telegram payments works.", reply_markup=kb.return_to_client_interface_kb)
