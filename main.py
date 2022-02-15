import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import requests
import bs4
import random

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

talk("Чем я могу Вам помочь?")

def tell_time():
    time = datetime.datetime.now()
    time = time.strftime("%I:%M")
    talk(time)

def tell_date():
    month = ["Января", "Февраля", "Марта", "Апреля",
             "Мая", "Июня", "Июля", "Августа", "Сентября",
             "Октября", "Ноября", "Декабря"]
    date = datetime.datetime.now()
    day = int(date.strftime("%d"))
    mon = int(date.strftime("%m"))
    # year = int(date.strftime("%y"))

    date = f'{day} {month[mon - 1]}' # {year}'
    talk(date)

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source)

def play_on_youtube(song):
    talk(f'Включаю {song}')
    pywhatkit.playonyt(song)

def get_anekdot():
    joke = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(joke.text, 'html.parser')

    jokes = soup.select('.anekdot_text')
    index = random.randrange(len(jokes))
    joke_text = jokes[index].get_text().strip()
    return joke_text

def tell_joke():
    talk('Внимание, анекдот!')
    joke_text = get_anekdot()
    talk(joke_text)

def take_command():
    try:
        with sr.Microphone() as source:
            print('Слушаю Вас ...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='ru-RU')
            print(f'Вы сказали: {command}')
            return command.lower()

    except:
        pass

def run():
    command = take_command()
    if "привет" in command:
        talk("Приветсвую Вас, мой тёмный Господин!!!")
    elif 'время' in command:
        tell_time()
    elif 'число' in command:
        tell_date()
    elif 'включи' in command:
        song = command.replace('включи ', '')
        play_on_youtube(song)
    elif 'анекдот' in command:
        tell_joke()

run()