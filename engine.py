import os
import requests
from json import dumps
import time

#ENVIRON'S
APP_URL = os.environ.get('APP_URL')
TOKEN = os.environ.get('TOKEN')
DARKSKY = os.environ.get('DARKSKY')
URL = 'https://api.telegram.org/bot' + TOKEN + '/'


#WEATHER
def getWeather():
    t = int(time.time())
    r = requests.get('https://api.darksky.net/forecast/{}/49.9992,36.2429,{}?lang=ru'.format(DARKSKY,t))
    r = r.json()
    r = r["currently"]

    type = r['precipType']
    clouds = r["cloudCover"] * 100
    temperature = round(r["apparentTemperature"]-32, 2)
    humidity = r["humidity"] * 100
    summary = r["summary"]

    return ("Погода ⛅\n"
          "<b>{0}</b>\n"
          "Облачность: {1}%\n"
          "Температура: {2} C\n"
          "Влажность: {3} %\n".format(summary, clouds, temperature, humidity))


#WIKISEARCH
def WikiSearch(search_request):
    link = 'https://ru.wikipedia.org/w/api.php/api.php?format=json&action=query&prop=extracts&titles={}' \
           '&redirects=true&format=json&exintro=false&exchars=1000&exlimit=1&exsectionformat=plain'.format(
        search_request)
    a = requests.get(link)
    res = a.json()

    res = res['query']['pages']
    res = res[next(iter(res.keys()))]
    res = res['extract']

    res = res[3:]
    res = res.replace('<br>', '\n')
    res = res.replace('<i>', '')
    res = res.replace('</i>', '')
    res = res.replace('<p>', '\n')
    res = res.replace('</p>', '')
    res = res.replace('<li>', '\n')
    res = res.replace('</li>', '')
    res = res.replace('<ul>', '\n')
    res = res.replace('</ul>', '')

    span_first = res.find('<span')
    span_second = res.rfind('/span>')

    if span_second != -1:
        span_second += 6

    res = res[:span_first] + res[span_second:]
    res = res.replace('<span>', '')
    res = res.replace('</span>', '')
    return res


#DUCKDUCKGO
def DuckDuckGo(search_request):
    a = requests.get('http://api.duckduckgo.com/?q={}&format=json&pretty=1'.format(search_request))
    res = a.json()
    res = res['Abstract']
    if res == '':
        res = 'Я ничего не нашла :('
    return res


#WEBHOOK
def setWebhook(app_url):
    url = URL + 'setWebhook?url='+app_url
    requests.get(url)


#TEXT
def sendMessage(chat_id, text, disable_notification=False, reply_markup='', disable_HTML=False):
    """
    '{"inline_keyboard":[[{"text":"Горизонтально", "callback_data":"horizontally"},' 
    '{"text":"Вертикально", "callback_data":"vertically"}]],"resize_keyboard":true}'
    :return:
    """
    if reply_markup:
        reply_markup = '&reply_markup=' + dumps(reply_markup)

    if disable_notification:
        disable_notification = '&disable_notification=true'
    else:
        disable_notification = ''

    if not disable_HTML:
        parse_mode='&parse_mode=HTML'
    else:
        parse_mode=''

    url = URL + 'sendMessage?chat_id={}&text={}{}{}{}'\
        .format(chat_id,text,parse_mode,reply_markup,disable_notification)
    res = requests.get(url)
    print(res.content)
    if res.ok:
        message_id = res.json()['result']['message_id']
        return message_id
    else:
        sendMessage(chat_id,str(res.content))
        return False


def sendChatAction(chat_id, action):
    """
    :param chat_id: int or str
    :param action: 'typing', or see in TELEGRAM API
    :return: True on success
    """
    url = URL + 'sendChatAction?chat_id={}&action={}'.format(chat_id, action)
    res = requests.get(url)
    if res.ok:
        return True
    else:
        return False


def answerCallbackQuery(callback_query_id,text):
    """
        callback_query_id = int
        text = str
        :return: True on success
    """
    url = URL + 'answerCallbackQuery?callback_query_id={}&text={}'\
        .format(callback_query_id, text)
    res = requests.get(url)
    if res.ok:
        return True
    else:
        return False


def editMessageReplyMarkup(chat_id,message_id,reply_markup):
    """
        callback_query_id = int
        text = str
        :return: True on success
    """
    reply_markup = dumps(reply_markup)
    url = URL + 'editMessageReplyMarkup?chat_id={}&message_id={}&reply_markup={}'\
        .format(chat_id,message_id, reply_markup)
    res = requests.get(url)
    print(res.content)
    if res.ok:
        return True
    else:
        return False


def editMessageText(chat_id,message_id,text,reply_markup=''):
    """
        callback_query_id = int
        text = str
        :return: True on success
    """
    if reply_markup != '':
        reply_markup = '&reply_markup=' + dumps(reply_markup)

    url = URL + 'editMessageText?chat_id={}&message_id={}&text={}&parse_mode=HTML{}'.format(chat_id,message_id, text, reply_markup)
    res = requests.get(url)
    if res.ok:
        return True
    else:
        return False


def editMessageCaption(chat_id,message_id,caption):
    """
        callback_query_id = int
        text = str
        :return: True on success
    """
    url = URL + 'editMessageCaption?chat_id={}&message_id={}&caption={}'.format(chat_id,message_id,caption)
    res = requests.get(url)
    if res.ok:
        return True
    else:
        return False


# STICKERS
def getStickerSet(name):
    url = URL + 'getStickerSet?name={}'.format(name)
    res = requests.get(url)
    return res.json()["result"]["stickers"]

def sendSticker(chat_id, sticker_id):
    url = URL + 'sendSticker?chat_id={}&sticker={}'.format(chat_id,sticker_id)
    requests.get(url)


# CHAT
def leaveChat(chat_id):
    res = URL + 'leaveChat?chat_id={}'.format(chat_id)
    requests.get(res)


def sendLocation(chat_id, lat, long):
    res = URL + 'sendLocation?chat_id={}&latitude={}&longitude={}'.format(chat_id, lat, long)
    requests.get(res)