import pywhatkit

def play_on_youtube(song):
    talk(f'Включаю {song}')
    pywhatkit.playonyt(song)
