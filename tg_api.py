import os
from dotenv import load_dotenv
import telegram


load_dotenv()


def make_post_at_tg_group(img_path: str, text: str = 'post text') -> None:
    tg_bot_api_token: str = os.getenv('TG_API_TOKEN')
    tg_chat_id: str = os.getenv('TG_CHAT_ID')

    tg_bot = telegram.Bot(token=tg_bot_api_token)

    with open(f'{img_path}', 'rb') as img:
        tg_bot.send_photo(chat_id=tg_chat_id, photo=img, caption=text)
