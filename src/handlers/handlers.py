from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext

from models.session import dbController
from models.models import User
from sqlalchemy import select
from .adminHandlers import addProduct, deleteProduct, changeProduct, seeAllProducts
from .clientHandlers import seeAllProducts, buyProduct
from settings.bot_init import dp, bot
from .state import Form
from .keyboards import kb

@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    await state.set_state(Form.default)
    
    session = dbController.get_session()
    with session() as s:
        
        user = s.query(User).filter(User.telegram_id == message.from_user.id).first()
        if user == None:
            user = User(
                tg_id = message.from_user.id,
                username = message.from_user.username
            )
            s.add(user)
            s.commit()
            
            
    

    await bot.send_message(message.from_user.id, 'This is test payments bot. Here you can try role of admin or client.', reply_markup=kb.start_kb)


@dp.callback_query_handler(text=['start_as_admin', 'admin_cancel', 'client_switch_to_admin'], state=[Form.see_all_products, Form.product_change_check, Form.change_name, Form.change_id, Form.default, Form.product_check, Form.delete_name, Form.delete_id])
async def adminInterface(callback_query: types.CallbackQuery, state: FSMContext):
    
    
    await bot.send_message(callback_query.from_user.id, 'admin interface', reply_markup=kb.admin_interface_kb)
    await callback_query.answer()



    await state.reset_state()
    await state.set_state(Form.admin_interface)
    
    

@dp.callback_query_handler(text=['start_as_client', 'client_cancel', 'admin_switch_to_client'], state=[Form.buy_id,Form.buy_name ,Form.see_all_products, Form.default, Form.admin_interface])
async def clientInterface(callback_query: types.CallbackQuery, state: FSMContext):
    
    await state.reset_state()

    await state.set_state(Form.client_interface)

    await bot.send_message(callback_query.from_user.id, 'client interface', reply_markup=kb.client_interface_kb)
    
    await callback_query.answer()

    