import json
import feedparser
from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request
import os
from urllib.parse import quote
from urllib.request import urlopen

# w oróżnieniu od wersji książkowej mamy jeden submit dla bu pól
# dodatkowo wpisanie tylko jednego wyszukiwania nie przywraca
# domyślnego wyniku dla drugiego
# każde nowe wyszukiwanie w dowolnym polu jest zapamiętywane jako nowe domyślne

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://classic.iol.co.za/cmlink/1.640',
             'epoznan': 'http://epoznan.pl/rss.php',
             }

DEAFAULTS = {'publication': 'epoznan',
             'city': 'Poznan,PL'
             }

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=04eae95ad58ff3d6b45089b57a134b32'


@app.route('/')
def get_home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEAFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEAFAULTS['city']
    else:
        DEAFAULTS['city'] = city
    weather = get_weather(city)
    return render_template('home.html', articles=articles, weather=weather)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEAFAULTS['publication']
    else:
        publication = query.lower()
        DEAFAULTS['publication'] = publication
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read().decode('utf-8')
    parsed = json.loads(data)
    weather = None

    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']}

    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
