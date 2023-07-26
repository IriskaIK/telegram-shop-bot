async def updateLastMessageId(state, bot, kb, callback_query = None, message = None):
    

    message_id = (await state.get_data('last_message_id')).get('last_message_id')
    
    print(message_id)
    if message_id == None:
        if(callback_query):
            await state.update_data(last_message_id = callback_query.message.message_id)
        elif(message):
            await state.update_data(last_message_id = message.message_id)

        return
    if(callback_query):
        print(message_id)
        await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=message_id, reply_markup=kb.empty_kb)
        await state.update_data(last_message_id = callback_query.message.message_id)

    elif(message):
        print(message_id)

        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=kb.empty_kb)
        await state.update_data( last_message_id = message.message_id)

    
async def removeKeyboardWithoutUpdateMessageId(state, bot, kb, callback_query = None, message = None):
    message_id = (await state.get_data('last_message_id')).get('last_message_id')
    
    
    if(callback_query):
        print(message_id)
        await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=message_id, reply_markup=kb.empty_kb)

    elif(message):
        print(message_id)

        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=kb.empty_kb)

