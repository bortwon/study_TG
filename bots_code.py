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



# ================ Bot №3 ("Угадай число") ==============================

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import Message
from config import config
import random


bot_token: str = config.bot_token.get_secret_value()

# Создаем объекты бота и диспетчера
bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
attempts: int = 5

# Словарь, в котором будут храниться данные пользователя
user: dict = {'in_game': False,
        'secret_number': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}

users: dict = {}

# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=['start']))
async def get_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = user


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def get_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {attempts} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def get_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def get_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def get_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = attempts
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def get_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def get_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Загаданное число меньше!')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Загаданное число больше!')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                                 f'сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def get_other_answers(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = user
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)



# =====================================================================