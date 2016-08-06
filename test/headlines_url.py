import os
import feedparser
from flask import Flask
from flask import send_from_directory
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://classic.iol.co.za/cmlink/1.640',
             'epoznan': 'http://epoznan.pl/rss.php',
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
    # możemy przekazać do szablonu całą listę słowników z feedami
    # odrobinę logiki (iterowanie po elementach) przerzucamy do szablonu
    # do klucza słownika w szablonie odwołujemy się za pomocą kropki
    return render_template('test/home_post.html', articles=feed['entries'])

    # first_article = feed['entries'][0]
    # zamiast first_article['title'] używamy get()
    # get() to metoda słownika, w razie braku klucza nie dostaniemy błędu
    # return """
    #     <html>
    #         <body>
    #             <h1>BBC Headlines</h1>
    #             <b>{0}</b>
    #             <br />
    #             <i>{1}</i>
    #             <br />
    #             <p>{2}</p>
    #             <br />
    #         </body>
    #     </html>
    # """.format(first_article.get('title'),
    #            first_article.get('published'),
    #            first_article.get('summary'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
