import datetime

time = datetime.datetime.now()
time = time.strftime("%I:%M")
print(time)

month = ["Января", "Февраля", "Марта", "Апреля",
         "Мая", "Июня", "Июля", "Августа", "Сентября",
         "Октября", "Ноября", "Декабря"]

date = datetime.datetime.now()
day = int(date.strftime("%d"))
mon = int(date.strftime("%m"))
year = int(date.strftime("%y"))

date = f'{day} {month[mon - 1]} {year}'
print(date)