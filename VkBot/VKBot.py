import vk_api
import time
import sys, traceback
import datetime
vk = vk_api.VkApi(token='ebbe94d588065027e84301a672516f07e3a39a454a638332786e69d7b2f6759e76840654993bb5d5a5eec')
vk._auth_token()

values = {'out':0, 'count':100, 'time_offset':60, 'group_id':160615635}
OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}


def eval_(formula):
    def parse(formula_string):
        number = ''
        for s in formula_string:
            if s in '1234567890.':
                number += s
            elif number:
                yield float(number)
                number = ''
            if s in OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]

    return calc(shunting_yard(parse(formula)))
def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id, 'message':s})

def now_wd():
        return datetime.datetime.now().weekday() + 1
def wd_string():
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return days[now_wd() - 1]
def now_mth():
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return months[datetime.datetime.now().month - 1]
while True:
    try:
        response = vk.method('messages.getConversations', values)
        #if response['items']:
        #values['last_message_id'] = response['items'][0]['id']
        for item in response['items']:

            #if vk.method('groups.isMember', item['last_message']['peer_id']) == 0:
            #    answer = 'Подпишись, иначе ты позорник :)'
            if item['last_message']['text']=="Привет!":
                answer = 'И вам привет!'
            elif item['last_message']['text'] == "Привет":
                answer = 'И вам привет!'
            elif item['last_message']['text'] == "Время":
                time = datetime.datetime.time(datetime.datetime.now())
                answer = str(time.hour) + ':' + str(time.minute)
            elif item['last_message']['text'] == "День":
                answer = 'Cегодня ' + wd_string()
            elif item['last_message']['text'] == "День по счету":
                answer = 'Cегодня ' + str(now_wd()) + ' день недели'
            elif item['last_message']['text'] == "Месяц":
                answer = now_mth()
            elif item['last_message']['text'] == "Пока":
                answer = 'Пока'
            elif item['last_message']['text'] == "Хей":
                answer = 'Салют братан'
            elif item['last_message']['text'] == "Как дела?":
                answer = 'Хорошо'
            elif item['last_message']['text'] == "Неверно":
                answer = 'Я отправлю сообщение админу'
                #write_msg(202205273, 'Срочно помоги - ')
                #print(vk.method('messages.getHistory', {'peer_id': item['last_message']['peer_id'], 'count': 200}))
            else:
                try:
                    answer = eval_(item['last_message']['text'])
                except:
                    answer = 'Не понял'
            write_msg(item['conversation']['peer']['local_id'], answer)
            #print(item['last_message']['from_id'])
            print(datetime.datetime.now(),'from id {} sent message = {} we answered = {}'.
            format(item['last_message']['from_id'],item['last_message']['text'],answer))
        time.sleep(0.5)
    except:
        pass