from vk_api import make_post_at_vk_group_wall
from tg_api import make_post_at_tg_group


def make_post(post_image_path: str, post_text: str, post_vk: str ='NO', post_ok: str ='NO', post_tg: str ='NO') -> str:
    """
    Размещает полученное изображение и текст в виде поста в соцсети с флагом 'YES'
    :param post_image_path: str: путь к файлу изображения
    :param post_text: str: путь к текстовому файлу с содержанием поста
    :param post_vk: str: флаг выбора соцсети YES/NO
    :param post_ok: str: флаг выбора соцсети YES/NO
    :param post_tg: : str: флаг выбора соцсети YES/NO
    :return: None
    """
    if post_vk == 'YES':
        try:
            post_vk_link = make_post_at_vk_group_wall(post_image_path, post_text)
        except Exception:
            post_vk_link: str = 'Error'
    else:
        post_vk_link: str = post_vk
    if post_tg == 'YES':
        try:
            post_tg_link = make_post_at_tg_group(post_image_path, post_text)
        except Exception:
            post_tg_link: str = 'Error'
    else:
        post_tg_link: str = post_tg

    return post_tg_link, post_vk_link
