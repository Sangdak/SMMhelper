from google_api import get_g_sheet_content, download_files_to_dirs, add_to_g_sheet
from poster import make_post
import time
from datetime import datetime
import os
from dotenv import load_dotenv


REFRESH_TABLE_PERIOD_IN_SECONDS: int = 10


def make_table_content() -> list[dict]:
    """Создаёт актуальный список задач на выполнение из гугл таблицы"""
    table_content = get_g_sheet_content()

    titles = ('row_num', 'pub_date', 'pub_time', 'img_link', 'text_link', 'post_vk', 'post_ok', 'post_tg', 'is_draft', 'is_posted')
    table_rows = []

    for table_row in table_content:
        if table_row[-1] != 'POSTED' and table_row[-2] == 'POST':
            table_rows.append(dict(zip(titles, table_row)))

    return table_rows


def get_text_from_file(text_path: str) -> str:
    """
    Получает содержание поста из соответствующего текстового файла в папке 'txts'
    :param text_path: str: Путь до текстового файла ('./txts/<file>')
    :return: str: Текст поста
    """
    with open(text_path) as text_file:
        post_text = text_file.read()
    return post_text


def main():
    load_dotenv()
    task_queue_lenght: int = 0

    while True:
        current_time = datetime.now().timetuple()
        current_hour_min = str(f'{current_time.tm_hour}:{current_time.tm_min}')
        print(current_hour_min)
        tasks_queue = make_table_content()
        print(tasks_queue)

        for task in tasks_queue:
            print(task['pub_date'], task['pub_time'][:-3])
            if task['pub_date'] == str(datetime.now().date()):

                if len(tasks_queue) != task_queue_lenght:
                    task_queue_lenght = len(tasks_queue)
                    download_files_to_dirs()

                if task['pub_time'][:-3] == current_hour_min:
                    img_path = f"./imgs/{task['img_link']}"
                    text = get_text_from_file(f"./txts/{task['text_link']}")

                    make_post(img_path, text, task['post_vk'], task['post_ok'], task['post_tg'])

                    add_to_g_sheet(task['row_num'])

        time.sleep(REFRESH_TABLE_PERIOD_IN_SECONDS)


if __name__ == '__main__':
    main()
