import engine as e
from random import choice
import datetime

schedule={
    0:"<b>Понедельник:</b>\n1. Английский 56/36 \n\n2. Укр.мова 56\n\n3. АСД 42\n\n4. Соц.мережi 43",
    1:"<b>Вторник:</b>\n1. Дискретка 33 \n\n2. Опер.системы 33\n\n3. КГ (Карпусь) 43",
    2:"<b>Среда:</b>\n1. ООП 65\n(перша пара Лысяк, everything is fucked)\n\n2. АСД 42\n\n3. Фезра С/З",
    3:"<b>Четверг:</b>\n1. Опер.системы 33 \n\n2. ООП 42\n\n3. Фезра С/З",
    4:"<b>Пятница:</b>\n1. АСД 42/Опер.системы 33\n\n2. КГ (Карпусь) 43\n\n3. Дискретка 33",
    5:"<b>ПИЙ ГОРIЛКУ, СЕГОДНЯ ВЫХОДНОЙ</b>\n(суббота)",
    6:"<b>ПИЙ ГОРIЛКУ, СЕГОДНЯ ВЫХОДНОЙ</b>\n(воскресенье)"
}

schedule_markup = {"inline_keyboard":
                      [[{"text": "Пн", "callback_data": "0"},
                        {"text": "Вт", "callback_data": "1"},
                        {"text": "Ср", "callback_data": "2"},
                        {"text": "Чт", "callback_data": "3"},
                        {"text": "Пт", "callback_data": "4"}]]
            , "resize_keyboard": True}

people_list = {
    'people1': """
1.Андрющенко Михайло Андрiйович
2.Бей Руслан Александрович
3.Вуciк Олег Юрiйович
4.Гордiенко Маргарита Романiвна
5.Дружинiна Марiя Олександрiвна
6.Зюбiн Iван Олексiйович
7.Iванов Артем Владиславович
8.Кондратьев Антон Андрiйович
9.Курашов Евгенiй Олександрович
10.Лещенко Андрюха Сергiйович
11.Максименков Олексiй Юрiйович
12.Мельтюхов Богдан Максимович
""",
    'people2': """
13.Орлов Микита Миколайович
14.Пелюшок Богдан Володимирович
15.Погоренко Наталiя Сергiiвна
16.Полторацька Анна Геннадiiвна
17.Рижков Кирило Павлович
18.Роздайвайфай Олег Юрiйович
19.Скрит Iрина Петрiвна
20.Хмелевський Евгенiй Володимирович
21.Хмельницький Даниiл Олександрович
22.Хоменко Iлля Сергiйович
23.Чайкiн Вiктор Владиславович
"""
}

people_list_markup = {"inline_keyboard":
                      [[{"text": "<<", "callback_data": "people1"},
                        {"text": ">>", "callback_data": "people2"}]]
            , "resize_keyboard": True}

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

    if text == "/start":
        e.sendMessage(chat_id,"._.")

    elif text == "/s":
        weekday = datetime.datetime.now().weekday()
        try:
            weekday = int(text[2:])
        except Exception:
            pass
        markup = schedule_markup
        e.sendMessage(chat_id,schedule[weekday],reply_markup=markup)

    elif text == "/l":
        e.sendMessage(chat_id,people_list['people1'],reply_markup=people_list_markup)


    elif text == "/danil":
        e.sendMessage(chat_id,"<b>ДЕБИЛ!!!</b>")

    elif text == "/hello":
        e.sendMessage(chat_id,"Привет")

    elif text == "/sex":
        e.sendMessage(chat_id,"И немного <i>секса</i>")

    elif text == "/andruxa":
        e.sendMessage(chat_id, 'ЕБАТЬ АНДРЮХА!')
        e.sendMessage(chat_id, 'МУЖИК!')
        e.sendMessage(chat_id, '😎😎😎')

    elif text == "/orlow":
        e.sendMessage(chat_id, 't.me/orlow')

    elif text == '/github':
        e.sendMessage(chat_id, 'Голые исходники <code>только с 18</code>'
                               '\nhttps://github.com/orlovw/karpikchan')

    elif text == "/ivan":
        e.sendMessage(chat_id, '<code>T S Y A R</code>')

    elif text == "/cookie":
        markup = {"inline_keyboard":
                      [[{"text": "Получить печенье 🍪", "callback_data": "999"}]]
            , "resize_keyboard": True}
        e.sendMessage(chat_id, "Я приготовила печеньки!", reply_markup=markup)

    elif text == "/anime":
        res = e.getStickerSet('catgirlnecoco2')
        sticker_list = [i["file_id"] for i in res]
        e.sendSticker(chat_id, choice(sticker_list))

    elif text == "/linux":
        e.sendMessage(chat_id, """
{0}: Полюбила я пингвина,
{0}: Не всего, а половину
{0}: - Половину нижнюю,
{0}: Яркую, подвижную )
{1}: Тоже с линупсом трахаесси?
        """.format("<b>404_user_not_found</b>","<b>xYZ</b>"))

    else:
        e.sendMessage(chat_id,"Я такого не знаю")




def callback_query_handler(query):

    print(query)

    chat_id = query['chat_id']
    data = query['data']
    message_id = query['message_id']
    callback_query_id = query["callback_query_id"]

    if data == '999':
        e.answerCallbackQuery(callback_query_id,'Забирай, мне не жалко :3')

    elif data[:6] == 'people':
        e.editMessageText(chat_id, message_id, people_list[data], reply_markup=people_list_markup)
        e.answerCallbackQuery(callback_query_id, 'Меняю список 🤗')

    else:
        data = int(data)
        e.editMessageText(chat_id,message_id,schedule[data],reply_markup=schedule_markup)
        e.answerCallbackQuery(callback_query_id, 'Меняю расписание 😽')

