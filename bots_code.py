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

# import requests
# import time
# import os
# import dotenv
#
# dotenv.load_dotenv()
#
# API_TG_URL: str = os.getenv('API_TG_URL')
# API_CATS_URL: str = os.getenv('API_CATS_URL')
# API_DOGS_URL: str = os.getenv('API_DOGS_URL')
# API_FOX_URL: str = 'API_FOX_URL'
# BOT_TOKEN: str = os.getenv('BOT_TOKEN')
# ERROR_TEXT: str = 'Здесь должна была быть картинка с пёсиком :('
#
# offset: int = -2
# counter: int = 0
# dog_response: requests.Response
# dog_link: str
#
# while counter < 100:
#     print('attempt =', counter)
#
#     updates = requests.get(f'{API_TG_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
#
#     if updates['result']:
#         msg_from_user = updates['result'][0]['message']['text']
#         text = f'"{msg_from_user}" это конечно интересно, но лучше посмотри на пёсика :)'
#         for result in updates['result']:
#             offset = result['update_id']
#             chat_id = result['message']['from']['id']
#             dog_response = requests.get(API_DOGS_URL)
#             if dog_response.status_code == 200:
#                 dog_link = dog_response.json()['url']
#                 requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
#                 requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={dog_link}')
#             else:
#                 requests.get(f'{API_TG_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
#     time.sleep(1)
#     counter += 1


# ======================================================