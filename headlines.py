from flask import Flask
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://classic.iol.co.za/cmlink/1.640'
             }


# funkcje nie muszą mieć takiej samej nazwy jak ścieżka
# nie wywołujemy funkcji bezpośrednio, jej nazwa nie ma specjalnego znaczenia
# nazwa funkcji nie może się powtarzać, zostanie użyta ostatnia zdefiniowana

# fragment url w naw. trójkątnych zostanie przekazany do funkcji jako zmienna
# zmienne url muszą być parametrami funkcji

@app.route('/')
@app.route('/<publication>')
def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return """
        <html>
            <body>
                <h1>BBC Headlines</h1>
                <b>{0}</b>
                <br />
                <i>{1}</i>
                <br />
                <p>{2}</p>
                <br />
            </body>
        </html>
    """.format(first_article.get('title'),
               first_article.get('published'),
               first_article.get('summary'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)