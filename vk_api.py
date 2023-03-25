import os
from dotenv import load_dotenv
from typing import Any
import requests


load_dotenv()


def make_post_at_vk_group_wall(img_path: str, text: str = 'post text') -> None:
    token: str = os.getenv('VK_ACCESS_TOKEN')
    group_id: str = os.getenv('VK_GROUP_ID')

    url_for_uploading = _get_photo_upload_link(group_id, token)

    with open(img_path, 'rb') as image:
        file = {'photo': image}

        upload_response = _upload_photo_to_the_server(url_for_uploading, file, group_id)

    photo = upload_response['photo']
    server = upload_response['server']
    img_hash = upload_response['hash']

    owner_id, photo_id = _upload_photo_at_wall(photo, server, img_hash, group_id, token)

    _post_photo_at_wall(owner_id, photo_id, text, group_id, token)


def _get_photo_upload_link(group_id: str, token: str) -> str:
    method = 'photos.getWallUploadServer'
    url = f'https://api.vk.com/method/{method}'

    payloads = {
        'group_id': group_id,
        'access_token': token,
        'v': 5.131,
    }

    response = requests.get(url, params=payloads)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def _upload_photo_to_the_server(url: str, file: dict, group_id: str) -> Any:
    params = {'group_id': group_id}

    response = requests.post(url, files=file, params=params)
    response.raise_for_status()
    return response.json()


def _upload_photo_at_wall(photo: str, server: str, img_hash: Any, group_id: str, token: str) -> Any:
    method = 'photos.saveWallPhoto'
    url = f'https://api.vk.com/method/{method}'
    payloads = {
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': img_hash,
        'access_token': token,
        'v': 5.131,
    }
    response = requests.post(url, params=payloads)
    response.raise_for_status()
    uploaded_photo = response.json()
    return uploaded_photo['response'][0]['owner_id'], uploaded_photo['response'][0]['id']


def _post_photo_at_wall(owner_id, photo_id, alt, group_id, token):
    full_photo_id = f'photo{owner_id}_{photo_id}'
    method = 'wall.post'
    url = f'https://api.vk.com/method/{method}'
    payloads = {
        'attachments': full_photo_id,
        'owner_id': f'-{group_id}',
        'from_group': 1,  # Posts are posted on behalf of the group.
        'message': alt,
        'access_token': token,
        'v': 5.131,
    }
    response = requests.post(url, params=payloads)
    response.raise_for_status()
    return response.json()
