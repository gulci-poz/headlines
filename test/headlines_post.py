import os
import feedparser
from flask import Flask
from flask import send_from_directory
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://classic.iol.co.za/cmlink/1.640',
             'epoznan': 'http://epoznan.pl/rss.php',
             }


# domyślnie jest tylko GET
# dodajemy POST i możemy korzystać z obu metod;
# z której skorzystamy, zostanie określone w formularzu html;
# korzystamy z post, dlatego wybieramy form z globalnego kontekstu request
# na wypadek braku pustego parametru mamy przypisanie domyślnej wartości
@app.route('/', methods=['GET', 'POST'])
def get_news():
    query = request.form.get('publication')

    # istnienie argumentu publication i obecności na liście RSS
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template('home.html', articles=feed['entries'])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
