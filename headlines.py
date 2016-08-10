import json
import feedparser
from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request
import os
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://classic.iol.co.za/cmlink/1.640',
             'epoznan': 'http://epoznan.pl/rss.php',
             }

DEAFAULTS = {'publication': 'bbc',
             'city': 'London,UK',
             'currency_from': 'GBP',
             'currency_to': 'USD'
             }

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=04eae95ad58ff3d6b45089b57a134b32'

CURRENCY_URL = 'https://openexchangerates.org/api/latest.json?app_id=fc18ae86450c488797f29715f22afdba'


@app.route('/')
def get_home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEAFAULTS['publication']
    articles = get_news(publication)

    city = request.args.get('city')
    if not city:
        city = DEAFAULTS['city']
    weather = get_weather(city)

    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEAFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEAFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template('home.html',
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies))


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
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    parsed = json.loads(data)
    weather = None

    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']}

    return weather


def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read().decode('utf-8')
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate / frm_rate, parsed.keys()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
