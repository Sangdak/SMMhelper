#  Основной файл для запуска приложения

from google_api import get_tasks_from_gtable, get_post_content_from_gdoc, get_post_img
from poster import make_post_tg, make_post_ok, make_post_vk
import time
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    #  id = {os.getenv('ID')}
    ...


if __name__ == '__main__':
    main()
