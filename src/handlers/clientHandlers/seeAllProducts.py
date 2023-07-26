from aiogram import types
from aiogram.dispatcher import FSMContext

from models.session import dbController
from models.models import Product
from settings.bot_init import dp, bot
# from handlers.handlers import dp
from .keyboards import kb
from ..state import Form
from .service.ResponseGenerator import generateClientProductResponse


@dp.callback_query_handler(text = 'client_see', state=[Form.client_interface])
async def SeeAllProducts(callback_query: types.CallbackQuery, state: FSMContext):
    
    
    await callback_query.answer()
    await state.set_state(Form.see_all_products)
    
    session = dbController.get_session()
    product = None
    with session() as s:
        product = s.query(Product).filter(Product.isSelling == True).all()
    
    response = generateClientProductResponse(product)
    
    await bot.send_message(callback_query.from_user.id, f'All products:\n{response}', reply_markup=kb.return_to_client_interface_kb)