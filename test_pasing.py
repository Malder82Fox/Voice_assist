import requests
import bs4
import random

joke = requests.get('http://anekdotme.ru/random')
soup = bs4.BeautifulSoup(joke.text, 'html.parser')

jokes = soup.select('.anekdot_text')
index = random.randrange(len(jokes))
joke_text = jokes[index].get_text().strip()

print(joke_text)