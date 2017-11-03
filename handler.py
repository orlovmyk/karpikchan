import engine as e
import constants
import datetime
import math
from random import choice

schedule = constants.schedule
schedule_markup = constants.schedule_markup
people_list = constants.people_list
people_list_markup = constants.people_list_markup

"""
        text = res['text']
        if not text:
            text = '<code>пост без сообщения</code>'

        attachments = res["attachments"]
        markup = []
        if attachments:
            for i in attachments:
                current_item = next(iter(i.items()))
                markup.append([{"text": current_item[0]}, {"callback_data": 'url'+current_item[1]}])

        e.sendMessage(chat_id, text,reply_markup= {"inline_keyboard": markup ,"resize_keyboard": True})
"""

def message_handler(query):
    """
    {'last_name': '🍀', 'chat_id': 239062390, 'first_name': 'orlow', 'username': 'orlow', 'text': '3'}
    
    markup_usage    
    markup = {"inline_keyboard":
                      [[{"text":"Горизонтально", "callback_data":"horizontally"},
                        {"text":"Вертикально", "callback_data":"vertically"}]]
            ,"resize_keyboard":True}
    
    """

    chat_id = query["chat_id"]

    if 'text' in query.keys():
        text = query["text"]
        text_message(chat_id, text)

    if 'location' in query.keys():
        location = query['location']
        location_message(chat_id, location)




def callback_query_handler(query):

    print(query)

    chat_id = query['chat_id']
    data = query['data']
    message_id = query['message_id']
    callback_query_id = query["callback_query_id"]

    if data == '999':
        e.answerCallbackQuery(callback_query_id,'Вы поулчили по ебалу')

    elif data[:6] == 'people':
        e.editMessageText(chat_id, message_id, people_list[data], reply_markup=people_list_markup)
        e.answerCallbackQuery(callback_query_id, 'Меняю список 🤗')

    else:
        data = int(data)
        e.editMessageText(chat_id,message_id,schedule[data],reply_markup=schedule_markup)
        e.answerCallbackQuery(callback_query_id, 'Меняю расписание 😽')


def text_message(chat_id, text):
    if '@' in text:
        res = text.find('@')
        text = text[:res]

    if text == "/s":
        weekday = datetime.datetime.now().weekday()
        markup = schedule_markup
        e.sendMessage(chat_id, schedule[weekday], reply_markup=markup)

    elif text == "/l":
        e.sendMessage(chat_id, people_list['people1'], reply_markup=people_list_markup)

    elif text == "/w":
        e.sendMessage(chat_id, e.getWeather())

    elif text[1] == "g":
        text = text[3:]
        e.sendMessage(chat_id, e.DuckDuckGo(text))

    elif text[1] == "i":
        text = text[3:]
        e.sendMessage(chat_id, e.WikiSearch(text))

    elif text == "/andruxa":
        e.sendMessage(chat_id, 'ЕБАТЬ АНДРЮХА!')
        e.sendMessage(chat_id, 'МУЖИК!')
        e.sendMessage(chat_id, '😎😎😎')

    elif text == "/cookie":
        markup = {"inline_keyboard":
                      [[{"text": "Получить печенье 🍪", "callback_data": "999"}]]
            , "resize_keyboard": True}
        e.sendMessage(chat_id, "Я приготовила печеньки!", reply_markup=markup)

    elif text == "/anime":
        stickers_rand = choice([ 'catgirlnecoco2',
                                 'catgirlnecoco3',
                                 'Usagikei',
                                 'Usagikei2'])
        res = e.getStickerSet(stickers_rand)
        sticker_list = [i["file_id"] for i in res]
        e.sendSticker(chat_id, choice(sticker_list))

    elif text == "/kurashow":
        res = e.getStickerSet('Kurashow')
        sticker_list = [i["file_id"] for i in res]
        e.sendSticker(chat_id, choice(sticker_list))

    elif text == "/map":
        e.sendMessage(chat_id,'Ну и как я считать без координат буду?',
                      reply_markup={"keyboard": [[{"text": "Мое местоположение", "request_location": True}]],
                                    "resize_keyboard": True, "one_time_keyboard": True})

    elif text == "/linux":
        e.sendMessage(chat_id, """
{0}: Полюбила я пингвина,
{0}: Не всего, а половину
{0}: - Половину нижнюю,
{0}: Яркую, подвижную )
{1}: Тоже с линупсом трахаесси?
            """.format("<b>404_user_not_found</b>", "<b>xYZ</b>"))

    elif text in constants.text_answers.keys():
        e.sendMessage(chat_id, constants.text_answers[text])

    else:
        answer = choice(['Я такого не знаю',
                        'Ну не понимаю!',
                        'Зачем задавать такие сложные вопросы?',
                        'Вы с меня смеетесь там наверное, да? :(',
                        'Еще один такой двузначный вопрос и я ливну!'])
        e.sendMessage(chat_id, answer)


def location_message(chat_id, data):
    lat = data['latitude']
    long = data['longitude']

    lat_k = constants.latitude
    long_k = constants.longitude

    res = location_calc(lat, long, lat_k, long_k)

    e.sendMessage(chat_id, 'До шараги {} км'.format(round(res / 1000, 2)))


def location_calc(lt1, lng1, lt2, lng2):

    EARTH_RADIUS = 6372795

    lat1 = lt1 * math.pi / 180
    long1 = lng1 * math.pi / 180
    lat2 = lt2 * math.pi / 180
    long2 = lng2 * math.pi / 180

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)

    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt((cl2 * sdelta)**2 + (cl1 * sl2 - sl1 * cl2 * cdelta)**2)
    x = sl1 * sl2 + cl1 * cl2 * cdelta

    ad = math.atan2(y, x)
    dist = ad * EARTH_RADIUS

    #в метрах
    return dist