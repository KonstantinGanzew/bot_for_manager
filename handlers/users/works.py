import logging
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import erp
from aiogram.dispatcher.filters.state import StatesGroup, State
import keybords.inline.choice_buttons as key
import keybords.inline.callback_datas as call_datas
from bd.sql import create_profile, all_tender, tender_9

# Кнопка старт, аутентифицирует человека, отправляет клавиатуру
@dp.message_handler(Command('start'))
async def show_menu(message: Message):
    text = '''Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.'''
    await message.answer(text, reply_markup=key.menu_keyboard)
    await create_profile(message.from_user.id, message.from_user.username)


# Кнопка для помощи
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='help'))
async def help_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text('Бот создан для сотрудников уфанета, на поиск новых тендеров, в данный момент поиск осуществляется только по сайту газпрома.\nПервый пункт выводит все активные тендеры с сайта,\nВторой пункт сортирует по типу Работы/Услуги\nТретий пункт можно подписаться на рассылку появившихся тендеров', reply_markup=key.help_keyboard)
    await call.answer()

# Кнопка для выхода из помощи
@dp.callback_query_handler(call_datas.help_callback.filter(item_help='back'))
async def help_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text('Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.', reply_markup=key.menu_keyboard)
    await call.answer()

# Отправляет все имеющиеся тендеры
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='view_all_tenders'))
async def view_all_tenders_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    res = await all_tender()
    for item in res:
        text = f'Имя: {item[1]}\nОписание: {item[2]}\nСсылка: {item[3]}\nНачал: {item[4]}\nКонец: {item[5]}\nТип тендера: {item[7]}'
        await bot.send_message(call.from_user.id, text)
    await bot.send_message(call.from_user.id, 'Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.', reply_markup=key.menu_keyboard)

# Отправляет все имеющиеся тендеры
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='works_services'))
async def view_all_tenders_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    res = await tender_9()
    for item in res:
        text = f'Имя: {item[1]}\nОписание: {item[2]}\nСсылка: {item[3]}\nНачал: {item[4]}\nКонец: {item[5]}\nТип тендера: {item[7]}'
        await bot.send_message(call.from_user.id, text)
    await bot.send_message(call.from_user.id, 'Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.', reply_markup=key.menu_keyboard)