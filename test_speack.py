import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[3].id)

engine.say("Привет я Ваш голосовой помошник")
engine.say("Чем я могу вам помочь?")
engine.runAndWait()

