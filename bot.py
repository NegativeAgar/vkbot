import vk_api # pip install vk_api
import time # Стандартный модуль Python
import random # Стандартный модуль Python
import re # Стандартный модуль Python
from memory_profiler import memory_usage # pip install memory_profiler
from datetime import datetime # pip install datetime
from time import sleep # Стандартный модуль Python [import time]
 
'''
Что-то не так? Есть вопросы?
Пиши сюда - https://vk.com/konyachkov777
'''
 
 
# Разные функции
 
# [ = Списки = ]
 
info_ = ['&#9989; Правда', '&#10062; Не правда'] # Команда - !инфа
 
 
# Авторизация
 
print('| Авторизация..')
 
#login, password = 'Логин', 'Пароль'
 
#vk_session = vk_api.VkApi(login, password)
token='339be2331f2029150468f344874f0cee100c15625eb71276b7daa12284b9ada002ec437003c05f6090401'
 
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
    print('| Авторизация прошла не успешно')
   
vk = vk_session.get_api()
 
print('| Авторизация прошла успешно')
 
# Переменные
 
values = {'out': 0, 'count': 1, 'time_offset': 60, 'peer_id': 2000000000, 'start_messages_id' : int()}
chat_id_ = 191138400#Тут ID Вашей беседы.
peer_id_ = 2000000000 # Тут математика. 2000000000 + ID Вашей беседы = 2000000001.
chat_title = vk.messages.getChat(chat_id=chat_id_)
chat_users = vk.messages.getChatUsers(chat_id=chat_id_)
chat_link = vk.messages.getInviteLink(peer_id=peer_id_)
time = time.strftime('%H:%M') # [import time]
now = datetime.now() # [import datetime]
 
# Админы
 

admin_2_level = [ruhasan]
admin_3_level = [shturman95]
admin_3_level = [veter_znakomo]
 
# циклы
 
 
 
# def
 
def send(chat_id, message): # Отправка сообщения
    vk.messages.send(chat_id=chat_id, message=message)
 
def send_photo(chat_id, message, attachment): # Отправка фотки
    vk.messages.send(chat_id=chat_id, message=message, attachment=attachment)
 
def send_sticker(chat_id, sticker_id): # Отправка стикеров
    vk.messages.sendSticker(chat_id=chat_id, sticker_id=sticker_id)
 
def change_chat_title(chat_id, title): # Команда - !название
    vk.messages.editChat(chat_id=chat_id, title=title)
 
def pin(peer_id): # Команда - ~ (закрепить сообщение)
    vk.messages.pin(peer_id=peer_id, message_id=response['items'][0]['id'])
 
def unpin(peer_id): # Команда - !~ (открепить сообщение)
    vk.messages.unpin(peer_id=peer_id_)
 
def chat_info(chat_id): # Команда - !инфа
    who = random.choice(info_) # [import random]
    vk.messages.send(chat_id=chat_id_, message= response['items'][0]['body'][5:] + ', ' + who)
 
 
def chat_lox(chat_id): # Команда - !лох
    id = random.choice(vk.messages.getChatUsers(chat_id=chat_id_))
    vk.messages.send(chat_id=chat_id_, message='@id' + str(vk.users.get(user_ids=id)[0]['id']) + '(' + str(vk.users.get(user_ids=id)[0]['first_name']) + ' ' +
                                              str(vk.users.get(user_ids=id)[0]['last_name']) + ') - сегодня лох.' )
 
                                         
while True:
    response = vk.messages.getHistory(out=values['out'], count=values['count'], peer_id=values['peer_id'], time_offset=values['time_offset'],
                              start_messages_id=values['start_messages_id'])
    for item in response['items']:
        if response ['items'][0]['body'] == '!меню':
            send(chat_id_, '| &#129302; Меню команд бота:\n\n| Команды для всех:\n\n  &#128312; !лох - Узнать кто сегодня лох\n  &#128312; !покинуть [Причина] - Покинуть беседу\n  &#128312; !рандом - Выдаёт случайное число и смайл\n  &#128312; !время - Узнать время и дату\n  &#128312; !инфа [Сообщение] - Узнать правду/не правду\n\n| Команды для Админов:\n\n  &#128312; !название [Название] - Изменить название беседы\n  &#128312; !очистить - Очистить чат беседы\n  &#128312; ~ [Сообщение] - Закрепить сообщение\n  &#128312; !~ - Открепить сообщение\n  &#128312; !кик [Выбрать сообщение] - Исключить участника беседы\n\n| Прочие команды:\n\n &#128312; Ожидайте')
        if response['items'][0]['body'] == '!лох':
            chat_lox(chat_id_)
        if response['items'][0]['body'] == '!ссылка' and response['items'][0]['user_id'] in admin_1_level:
            send(chat_id_, 'Ссылка на эту беседу: ' + str(chat_link['link']))
        if response['items'][0]['body'] == '!ссылка' and not response['items'][0]['user_id'] in admin_1_level:
            send(chat_id_, '&#10062; Вам недоступна данная команда.')
        if response['items'][0]['body'][0:9] == '!название' and response['items'][0]['user_id'] in admin_1_level:
            change_chat_title(chat_id_, response['items'][0]['body'][9:])
        if response['items'][0]['body'] == '!название' and not response['items'][0]['user_id'] in admin_1_level:
            send(chat_id_, '&#10062; Вам недоступна данная команда.')
        if response['items'][0]['body'] == '!очистить' and response['items'][0]['user_id'] in admin_1_level:
            send(chat_id_, '&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n&#4448;\n')
            send(chat_id_, '&#9989; Очищено!')
        if response['items'][0]['body'] == '!очистить' and not response['items'][0]['user_id'] in admin_1_level:
            send(chat_id_, '&#10062; Вам недоступна данная команда.')
        if response['items'][0]['body'][0:1] == '~' and response['items'][0]['user_id'] in admin_2_level:
            pin(peer_id_)
        if response['items'][0]['body'][0:1] == '~' and not response['items'][0]['user_id'] in admin_2_level:
            send(chat_id_, '&#10062; Вам недоступна данная команда.')
        if response['items'][0]['body'] == '!~' and response['items'][0]['user_id'] in admin_2_level:
            unpin(peer_id_)
        if response['items'][0]['body'] == '!~' and not response['items'][0]['user_id'] in admin_2_level:
            send(chat_id_, '&#10062; Вам недоступна данная команда.')
        if response['items'][0]['body'][0:9] == '!покинуть':
            vk.messages.removeChatUser(chat_id=chat_id_, user_id=response['items'][0]['user_id'])
            send(chat_id_,'@id' + str(vk.users.get(user_ids=response['items'][0]['user_id'])[0]['id']) + '(' + str(vk.users.get(user_ids=response['items'][0]['user_id'])[0]['first_name'] + ' ' + str(vk.users.get(user_ids=response['items'][0]['user_id'])[0]['last_name'] + ') - покинул беседу по причине: ' + response['items'][0]['body'][9:])))
        if re.match('!кик', response['items'][0]['body']) and response['items'][0]['user_id'] in admin_2_level:
            vk.messages.removeChatUser(chat_id=chat_id_, user_id=response['items'][0]['fwd_messages'][0]['user_id'])
        if response['items'][0]['body'] == '!рандом':
            sleep(2) # [from sleep import time]
            send(chat_id_,'Рандом: ' + str(random.randint(0,200))) # [import random]
        if response['items'][0]['body'] == '!бот тут?':
            send(chat_id_, 'На месте B-)')
        if response['items'][0]['body'] == '!время':
            send(chat_id_, '&#9200; Время: ' + str(time) + ' ' + '&#128467; Дата: ' + now.strftime('%d.%m.%y')) # [import time & datetime]
        if response['items'][0]['body'][0:5] == '!инфа':
            chat_info(chat_id_)