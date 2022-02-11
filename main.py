import speech_recognition as sr

listener = sr.Recognizer()

with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source)

try:
    with sr.Microphone() as source:
        print('Слушаем Вас ...')
        voice = listener.listen(source)
        command = listener.recognize_google(voice, language='ru-RU')
        print(f'Вы сказали: {command}')


except:
    pass

