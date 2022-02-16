import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import requests
import bs4
import random
import vk_api
import pyowm
import os
import config

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[3].id)

# engine.say("Привет я Ваш голосовой помошник")
# engine.say("Чем я могу вам помочь?")
# engine.runAndWait()

def talk(text):
    engine.say(text)
    engine.runAndWait()

talk(f'Чем я могу Вам помочь, {config.user_name}?')

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source)

def take_command():
    try:
        with sr.Microphone() as source:
            print('Слушаю ...')
            voice = listener.listen(source, timeout=1, phrase_time_limit=2)
            command = listener.recognize_google(voice, language='ru-RU').lower()
            for name in config.names:
                if name in command:
                    talk(f'Чем могу быть полезен, {config.user_name}?')
                    return take_vouce()
    except:
        pass
    return ''

def take_vouce():
    try:
        with sr.Microphone() as source:
            print('Слушаю ...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='ru-RU').lower()
            return command
    except:
        pass
    return ''

def tell_time():
    time = datetime.datetime.now()
    time = time.strftime("%I:%M")
    talk(time)

def tell_date():
    date = datetime.datetime.now()
    day = int(date.strftime("%d"))
    mon = int(date.strftime("%m"))
    # year = int(date.strftime("%y"))

    date = f'{day} {config.month[mon - 1]}'  # {year}'
    talk(date)

def play_on_youtube(song):
    talk(f'Включаю {song}')
    pywhatkit.playonyt(song)


def get_anekdot():
    joke = requests.get(config.jokes_url)
    soup = bs4.BeautifulSoup(joke.text, 'html.parser')

    jokes = soup.select('.anekdot_text')
    index = random.randrange(len(jokes))
    joke_text = jokes[index].get_text().strip()
    return joke_text


def tell_joke():
    talk('Внимание, анекдот!')
    joke_text = get_anekdot()
    talk(joke_text)

def vk_init():
    token = config.vk_token
    vk_session = vk_api.VkApi(token=token)
    return vk_session.get_api()

def get_new_messages():
    answer = []
    vk = vk_init()
    conversations = vk.messages.getConversations(offsets=0, count=20)
    for item in conversations['items']:
        try:
            unread_count = item['conversation']['unread_count']
            # print(unread_count)
            dialog_id = item['conversation']['peer']['local_id']
            conversation = vk.messages.getHistory(
                peer_id=dialog_id,
                count=unread_count,
                extended=True
            )

            profile = conversation['profiles'][0]
            user = f"{profile['first_name']} {profile['last_name']}"

            messages = conversation['items']
            messages.reverse()

            text = ''
            for message in messages:
                text += message['text'] + '\n'
            answer.append(f'{unread_count} сообщение от пользователя {user}:\n{text}')
        except:
            pass
    return answer

def check_vk():
    messages = get_new_messages()
    if len(messages) > 0:
        for message in messages:
            talk(message)
    else:
        talk(f'Нет новых сообщений, {config.user_name}')

def write_message_vk(user, msg):
    vk = vk_init()

    try:
        friends = vk.friends.search(user_id=config.vk_id, q=user)
        friend_id = friends['items'][0]['id']
        vk.messages.send(user_id=friend_id, message=msg, random_id=0)
    except IndexError:
        talk('Сорянчик такой юзер не найден')

def tell_weather():
    token = config.weather_token

    owm = pyowm.OWM(token)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(config.weather_city)

    weather = observation.weather
    talk(f"На улице {round(weather.temperature('celsius')['temp'])} градусов, ветер {round(weather.wind()['speed'])} метров")

def turn_radio():
    talk('Начинаем танцевать !!!')

    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)

    os.system('top_radio_top_40.m3u')

def turn_alarm():
    time = datetime.datetime.now()
    now_hour = time.hour
    now_minute = time.minute

    alarm_hour = int(config.alarm_time[:2])
    alarm_minute = int(config.alarm_time[2:])

    if now_hour == alarm_hour and now_minute == alarm_minute:
        config.alarm_status = False
        talk('Рота подъём !!!')

    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)

    os.system('top_radio_top_40.m3u')

def run():
    command = take_command()
    if "привет" in command:
        talk(f'Приветсвую Вас, {config.user_name}')
    elif 'время' in command:
        tell_time()
    elif 'день' in command:
        tell_date()
    elif 'включи' in command:
        song = command.replace('включи ', '')
        play_on_youtube(song)
    elif 'анекдот' in command:
        tell_joke()
    elif 'проверь' in command:
        check_vk()
    elif 'напиши' in command:
        talk('Кому написать?')
        user = take_vouce()
        talk('Что написать?')
        message = take_vouce()
        write_message_vk(user, message)
    elif 'погода' in command:
        talk('Погода сегодня')
        tell_weather()
    elif 'музыку' in command:
        turn_radio()
    elif 'будильник' in command:
        talk(f'{config.user_name}, на какое время поставить будильник?')
        config.alarm_time = take_vouce().replace(':', '')
        config.alarm_status = True
        # talk(f'будильник поставлен на {alarm_hour} часов и {alarm_minute} минут')

while True:
    run()
