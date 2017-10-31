import vk_api
import engine as e
import constants
import datetime
from random import choice

schedule = constants.schedule
schedule_markup = constants.schedule_markup
people_list = constants.people_list
people_list_markup = constants.people_list_markup

def message_handler(query):
    """
    {'last_name': '🍀', 'chat_id': 239062390, 'first_name': 'orlow', 'username': 'orlow', 'text': '3'}
    
    markup_usage    
    markup = {"inline_keyboard":
                      [[{"text":"Горизонтально", "callback_data":"horizontally"},
                        {"text":"Вертикально", "callback_data":"vertically"}]]
            ,"resize_keyboard":True}
    
    """

    text = query["text"]
    chat_id = query["chat_id"]

    if '@' in text:
        res = text.find('@')
        text = text[:res]

    if text == "/s":
        weekday = datetime.datetime.now().weekday()
        markup = schedule_markup
        e.sendMessage(chat_id,schedule[weekday],reply_markup=markup)

    elif text == "/l":
        e.sendMessage(chat_id,people_list['people1'],reply_markup=people_list_markup)

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
        res = e.getStickerSet('catgirlnecoco2')
        sticker_list = [i["file_id"] for i in res]
        e.sendSticker(chat_id, choice(sticker_list))

    elif text == "/time":
        res = datetime.time.microsecond

    elif text[:3] == '/vk':

        try:
            url = text[3:]
        except ValueError:
            e.sendMessage(chat_id,'Вы что-то напутали!')
            return

        res = vk_api.make_request(url)

        text = res['text']
        if text == '':
            text = '<code>пост без сообщения</code>'

        attachments = res["attachments"]
        markup = []
        if attachments:
            for i in attachments.items():
                markup.append([{"text":i[0]},{"callback_data":'url'+i[1]}])

        e.sendMessage(chat_id, text,reply_markup= {"inline_keyboard": markup ,"resize_keyboard": True})

    elif text == "/quit":
        e.sendMessage(chat_id, "Вы все здесь пидорасы!!!")
        e.leaveChat(chat_id)

    elif text == "/linux":
        e.sendMessage(chat_id, """
{0}: Полюбила я пингвина,
{0}: Не всего, а половину
{0}: - Половину нижнюю,
{0}: Яркую, подвижную )
{1}: Тоже с линупсом трахаесси?
        """.format("<b>404_user_not_found</b>","<b>xYZ</b>"))

    elif text in constants.text_answers.keys():
        e.sendMessage(chat_id,constants.text_answers[text])

    else:
        e.sendMessage(chat_id,"Я такого не знаю")




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

    elif data[:3] == 'url':
        e.sendMessage(chat_id, data[3:])

    else:
        data = int(data)
        e.editMessageText(chat_id,message_id,schedule[data],reply_markup=schedule_markup)
        e.answerCallbackQuery(callback_query_id, 'Меняю расписание 😽')

