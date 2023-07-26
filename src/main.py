from aiogram.utils import executor
from handlers.handlers import dp


from models.session import dbController
from models.models import User, Product, Order


executor.start_polling(dp, skip_updates = True)
session = dbController.get_session()

