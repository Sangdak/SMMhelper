import os
from dotenv import load_dotenv
import telegram


load_dotenv()


def make_post_at_tg_group(img_path: str, text: str = 'post text') -> str:
    tg_bot_api_token: str = os.getenv('TG_API_TOKEN')
    tg_chat_id: str = os.getenv('TG_CHAT_ID')

    tg_bot = telegram.Bot(token=tg_bot_api_token)

    with open(f'{img_path}', 'rb') as img:
        message = tg_bot.send_photo(chat_id=tg_chat_id, photo=img, caption=text)
        message_id = message.message_id

        return f'https://t.me/{tg_chat_id[1:]}/{message_id}'
