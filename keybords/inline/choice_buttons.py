from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keybords.inline.callback_datas as key

menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Помощь', callback_data=key.menu_callback.new(item_menu='help')),
        ],
        [
            InlineKeyboardButton(text='Посмотреть все тендеры', callback_data=key.menu_callback.new(item_menu='view_all_tenders')),
        ],
        [
            InlineKeyboardButton(text='Посмотреть все тендеры с типом "Работы/Услуги"', callback_data=key.menu_callback.new(item_menu='works_services')),
        ],
        [
            InlineKeyboardButton(text='Подписаться на рассылку', callback_data=key.menu_callback.new(item_menu='subscribe_to_newsletter')),
        ],
    ]
)

help_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Назад', callback_data=key.help_callback.new(item_help='back')),
        ],
    ]
)

