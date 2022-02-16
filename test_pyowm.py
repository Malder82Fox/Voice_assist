import pyowm

token = 'a0fce1f438ae6ac455ecd1435c3eaa9a'

owm = pyowm.OWM(token)
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Vsevolozhsk')

weather = observation.weather
print(f"На улице {round(weather.temperature('celsius')['temp'])} градусов, ветер {weather.wind()['speed']} метров в секунду")