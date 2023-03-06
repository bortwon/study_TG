#============================ BOT_1 ===============================

# Отправляет на все сообщения фото котиков

import requests
import time
import os
import dotenv

dotenv.load_dotenv()

API_TG_URL: str = os.getenv('API_TG_URL')
API_CATS_URL: str = os.getenv('API_CATS_URL')
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
ERROR_TEXT: str = 'Здесь должна была быть картинка с котиком :('

offset: int = -2
counter: int = 0
cat_response: requests.Response
cat_link: str


while counter < 100:
    print('attempt =', counter)

    updates = requests.get(f'{API_TG_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        msg_from_user = updates['result'][0]['message']['text']
        text = f'"{msg_from_user}" это конечно интересно, но лучше посмотри на котика :)'
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()['file']
                requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
                requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
    time.sleep(1)
    counter += 1


# Отправляет на все сообщения пёсиков

import requests
import time
import os
import dotenv

dotenv.load_dotenv()

API_TG_URL: str = os.getenv('API_TG_URL')
API_CATS_URL: str = os.getenv('API_CATS_URL')
API_DOGS_URL: str = os.getenv('API_DOGS_URL')
API_FOX_URL: str = 'API_FOX_URL'
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
ERROR_TEXT: str = 'Здесь должна была быть картинка с пёсиком :('

offset: int = -2
counter: int = 0
dog_response: requests.Response
dog_link: str

while counter < 100:
    print('attempt =', counter)

    updates = requests.get(f'{API_TG_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        msg_from_user = updates['result'][0]['message']['text']
        text = f'"{msg_from_user}" это конечно интересно, но лучше посмотри на пёсика :)'
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            dog_response = requests.get(API_DOGS_URL)
            if dog_response.status_code == 200:
                dog_link = dog_response.json()['url']
                requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
                requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={dog_link}')
            else:
                requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
    time.sleep(1)
    counter += 1


# =============================== BOT 2 (Эхо-бот) ===============================

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import Sticker
from aiogram import F
from config import config

bot_token: str = config.bot_token.get_secret_value()

bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


@dp.message(F.photo)
async def process_send_photo(message: Message):
    await message.reply_photo(message.photo[0].file_id)


@dp.message()
async def process_send_sticker(message: Message):
    await message.reply_sticker(message.sticker.file_id)


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)


# Полноценный Эхо-бот

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import config


bot_token: str = config.bot_token.get_secret_value()

bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается '
                                 'методом send_copy')

if __name__ == '__main__':
    dp.run_polling(bot)