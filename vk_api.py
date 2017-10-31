import requests
import os

TOKEN_VK = os.environ.get('TOKEN_VK')


def parse(data):
    data = data["response"][1]
    text = data["text"]
    attachments = []

    for i in data["attachments"]:
        type = i["type"]
        attachments.append({type: i[type]['src']})

    return {
        "text": text,
        "attachments": attachments
    }


def make_request(domain, offset=1):
    URL = 'https://api.vk.com/method/wall.get?domain={}&offset={}&count=1&access_token={}&v=V'\
        .format(domain, offset, TOKEN_VK)
    try:
        res = requests.get(URL)
    except requests.exceptions.ConnectionError:
        return None

    res = res.json()
    if 'error' in res.keys():
        return None

    try:
        res = parse(res)
    except Exception:
        return None

    return res

