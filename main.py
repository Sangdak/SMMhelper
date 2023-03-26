from poster import make_post

import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import time
import requests

from google_api import get_g_sheet_content, download_files_to_dirs, add_to_g_sheet


def make_table_content() -> list[dict]:
    """Создаёт актуальный список задач на выполнение из гугл таблицы"""
    table_rows = []
    titles = ('row_num', 'pub_date', 'pub_time', 'img_link', 'text_link',
              'post_vk', 'post_ok', 'post_tg', 'is_draft', 'is_posted',)

    table_content = get_g_sheet_content()

    for table_row in table_content:
        if table_row[-1] != 'POSTED' and table_row[-2] == 'POST':
            table_rows.append(dict(zip(titles, table_row)))

    return table_rows


def get_text_from_file(text_path: str) -> str:
    """ Получает содержание поста из соответствующего текстового файла в папке 'txts'
    :param text_path: str: Путь до текстового файла ('./txts/<file>')
    :return: str: Текст поста
    """
    with open(text_path) as text_file:
        post_text = text_file.read()
    return post_text


def get_img_from_link(img_url: str, img_folder: str) -> str:
    """Скачивает изображение по ссылке и сохраняет в соответствующую папку"""
    img_name = img_url.split('/')[-1]

    response = requests.get(img_url)
    response.raise_for_status()

    filepath = Path.cwd() / img_folder / img_name
    with open(filepath, "wb") as img_file:
        img_file.write(response.content)
    return img_name


def main():
    load_dotenv()

    refresh_table_seconds = int(os.getenv('REFRESH_TABLE_PERIOD_IN_SECONDS'))
    imgs_store_folder: str = os.getenv('IMAGES_FOLDER_NAME')
    task_queue_lenght: int = 0

    while True:
        current_time = datetime.now().timetuple()
        current_hour_and_min = str(f'{current_time.tm_hour}:{current_time.tm_min}')

        tasks_queue = make_table_content()

        for task in tasks_queue:
            if task['pub_date'] == str(datetime.now().date()):  # Если текущая дата совпадает с датой в строке

                if len(tasks_queue) != task_queue_lenght:  # Если количество задач отличается от прошлой итерации
                    task_queue_lenght = len(tasks_queue)
                    download_files_to_dirs()  # Загружаются изображения и текстовые файлы с гугл-диска

                if task['pub_time'][:-3] == current_hour_and_min:  # Текущее время (Часы и минуты) совпадает с заданием
                    if '/' in task['img_link']:
                        image_name = get_img_from_link(task['img_link'], imgs_store_folder)
                        img_path = f"./{imgs_store_folder}/{image_name}"
                    else:
                        img_path = f"./{imgs_store_folder}/{task['img_link']}"
                    text = get_text_from_file(f"./txts/{task['text_link']}")

                    post_tg_link = ''
                    post_vk_link = ''

                    try:
                        post_tg_link, post_vk_link = make_post(
                            img_path,
                            text,
                            task['post_vk'],
                            task['post_ok'],
                            task['post_tg']
                        )
                    except Exception:
                        pass
                    finally:
                        add_to_g_sheet(task['row_num'], post_tg_link, post_vk_link)

        time.sleep(refresh_table_seconds)


if __name__ == '__main__':
    main()
