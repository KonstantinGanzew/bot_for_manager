import logging
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
import erp
import keybords.inline.choice_buttons as key
import keybords.inline.callback_datas as call_datas
from bd.sql import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    await call.answer()

# Отправляет все имеющиеся тендеры
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='works_services'))
async def view_all_tenders_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    res = await tender_9()
    for item in res:
        text = f'Имя: {item[1]}\nОписание: {item[2]}\nСсылка: {item[3]}\nНачал: {item[4]}\nКонец: {item[5]}\nТип тендера: {item[7]}'
        await bot.send_message(call.from_user.id, text)
    await bot.send_message(call.from_user.id, 'Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.', reply_markup=key.menu_keyboard)
    await call.answer()

# Регистрация человеков
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='subscribe_to_newsletter'))
async def subscribe_to_newsletter_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    res = await mailing_status(str(call.from_user.id))
    text = 'Подписаться на рассылку'
    subscribe_newsletter = 'subscribe to newsletter'
    if res[0][0] == 2:
        text = 'Отписаться от рассылки'
        subscribe_newsletter = 'cancel_subscription'
    subscribe_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text=text, callback_data=call_datas.subscribe_to_newsletter_callback.new(item_subscribe_to_newsletter=subscribe_newsletter)),
            ],
            [
                InlineKeyboardButton(text='Главное меню', callback_data=call_datas.subscribe_to_newsletter_callback.new(item_subscribe_to_newsletter='main_menu')),
            ]
        ]
    )
    await call.message.edit_text('Вернуться в главное меню', reply_markup=subscribe_keyboard)
    await call.answer()

# Обработка регистрации на подписку
@dp.callback_query_handler(call_datas.subscribe_to_newsletter_callback.filter(item_subscribe_to_newsletter='subscribe to newsletter'))
async def sub_news(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    await get_mailing(call.from_user.id, 2)
    await call.message.edit_text('Вы подписались на рассылку', reply_markup=key.main_menu_keyboard)
    await call.answer()

# Обработка регистрации на отписку
@dp.callback_query_handler(call_datas.subscribe_to_newsletter_callback.filter(item_subscribe_to_newsletter='cancel_subscription'))
async def sub_news(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    await get_mailing(call.from_user.id, 1)
    await call.message.edit_text('Вы отписались от рассылки', reply_markup=key.main_menu_keyboard)
    await call.answer()

# Главное меню
@dp.callback_query_handler(call_datas.subscribe_to_newsletter_callback.filter(item_subscribe_to_newsletter='main_menu'))
async def main_menu(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    await call.message.edit_text('Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.', reply_markup=key.menu_keyboard)
    await call.answer()

@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='main'))
async def main_menu(call: CallbackQuery, callback_data: dict):
    logging.info(f'call + {callback_data}')
    await call.message.edit_text('Добро пожаловать\n\nЭто бот для просмотра всех активных тендеров.', reply_markup=key.menu_keyboard)
    await call.answer()
