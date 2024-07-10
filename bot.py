
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests, json
from requests.auth import HTTPBasicAuth
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from translations import translations


API_TOKEN = '7425916033:AAEzqfS3Yr_zSUJVxL6nFnH9BaynPZCJ0Ws'
DATABASE_PATH = '/db.sqlite3'
DJANGO_API_URL = 'http://192.168.1.43:8000/api/shipments/?tracking_code='
AUTH_USERNAME = 'admin'
AUTH_PASSWORD = 'admin'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_languages = {}

language_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
language_keyboard.add(KeyboardButton('🇬🇧 English'), KeyboardButton('🇺🇿 O\'zbek'), KeyboardButton('🇷🇺 Русский'))

def get_menu_keyboard(language):
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(translations[language]['get_tracking_info']),
        KeyboardButton(translations[language]['leave_comment']),
        KeyboardButton(translations[language]['address_contacts']),
        KeyboardButton(translations[language]['leave_request']),
        KeyboardButton(translations[language]['choose_language']),
        )  # Add "Get Tracking Info" button in a new row

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(translations['en']['start_message'], reply_markup=language_keyboard)

@dp.message_handler(lambda message: message.text in ['🇬🇧 English', '🇺🇿 O\'zbek', '🇷🇺 Русский'])
async def set_language(message: types.Message):
    if message.text == '🇬🇧 English':
        user_languages[message.from_user.id] = 'en'
    elif message.text == '🇺🇿 O\'zbek':
        user_languages[message.from_user.id] = 'uz'
    else:
        user_languages[message.from_user.id] = 'ru'
    
    language = user_languages[message.from_user.id]
    await message.reply(translations[language]['language_selected'], reply_markup=get_menu_keyboard(language))

@dp.message_handler(lambda message: message.text in ['💬 Leave a comment', '💬 Izoh qoldiring', '💬 Оставить комментарий'])
async def leave_comment(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply("You selected 'Leave a comment'. (Implement your logic here)")
    

@dp.message_handler(lambda message: message.text in ['📞 Address and contacts', '📞 Manzil va kontaktlar', '📞 Адрес и контакты'])
async def address_contacts(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply("You selected 'Address and contacts'. (Implement your logic here)")

@dp.message_handler(lambda message: message.text in ['📃 Leave a request', '📃 Ariza qoldiring', '📃 Оставить заявку'])
async def leave_request(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply("You selected 'Leave a request'. (Implement your logic here)")

@dp.message_handler(lambda message: message.text in ['🌎 Choose a language', '🌎 Tilni tanlang', '🌎 Выберите язык'])
async def choose_language(message: types.Message):
    await message.reply(translations['en']['start_message'], reply_markup=language_keyboard)
    

@dp.message_handler(lambda message: message.text in ['Get Tracking Info', 'Kuzatuv ma\'lumoti', 'Получить информацию о трекинге'])
async def get_tracking_info_button(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply("Please enter the tracking code to get information.")

@dp.message_handler()
async def get_tracking_info(message: types.Message):
    user_id = message.from_user.id
    language = user_languages.get(user_id, 'uz')  # Default to English if not set
    
    tracking_code = message.text.strip()
    response = requests.get(
        f"{DJANGO_API_URL}{tracking_code}",
        auth=HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD)
    )
    
    if response.status_code == 200:
        data = response.json()
        if data:  # Check if data is not empty
            reply_text = ""
            for item in data:
                reply_text += translations[language]['tracking_info'].format(
                    tracking_code=item['tracking_code'],
                    customer=item['customer'],
                    shipping_name=item['shipping_name'],
                    quantity=item['quantity'],
                    weight=item['weight'],
                    package_number=item['package_number'],
                    flight=item['flight']
                )
        else:
            reply_text = translations[language]['tracking_not_found']
    else:
        reply_text = translations[language]['error_message']
    
    await message.reply(reply_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)