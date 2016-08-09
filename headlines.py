import json
import feedparser
from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request
import os
from urllib.parse import quote
from urllib.request import urlopen

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://classic.iol.co.za/cmlink/1.640',
             'epoznan': 'http://epoznan.pl/rss.php',
             }

DEAFAULTS = {'publication': 'bbc',
             'city': 'Poznan,PL'
             }


@app.route('/')
def get_news():
    # args jest dla metody GET
    query = request.args.get('publication')

    # istnienie argumentu publication i obecności na liście RSS
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather('Poznan,PL')
    return render_template('home.html', articles=feed['entries'], weather=weather)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


def get_weather(query):
    # lokalizację będziemy mieli w {}
    # np. Poznan,PL
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=04eae95ad58ff3d6b45089b57a134b32'
    # lokalizację odzieramy ze spacji i przecinka
    query = quote(query)
    # formatujemy url, podstawiając przygotowaną lokalizację
    url = api_url.format(query)
    # ściągamy dane z przygotowanego urla, dostaniemy obiekt HTTPResponse w postaci bajtów
    data = urlopen(url).read().decode('utf-8')
    # parsujemy dane do json
    parsed = json.loads(data)
    # musimy zainicjować zmienną tutaj, jeśli zrobimy to w if, to zmienna będzie lokalna dla segmentu if
    weather = None

    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name']}

    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
