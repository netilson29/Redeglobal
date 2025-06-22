from flask import Flask, render_template
import feedparser
import time

app = Flask(__name__)

CACHE = {
    'noticias': [],
    'ultimo_update': 0
}

FEED_URL = "https://g1.globo.com/rss/g1/"

def pegar_noticias():
    agora = time.time()
    if agora - CACHE['ultimo_update'] > 1200:  # 20 minutos
        feed = feedparser.parse(FEED_URL)
        noticias = []
        for entrada in feed.entries[:12]:
            noticias.append({
                'titulo': entrada.title,
                'link': entrada.link,
                'resumo': entrada.summary,
                'imagem': entrada.get('media_content', [{}])[0].get('url', '')
            })
        CACHE['noticias'] = noticias
        CACHE['ultimo_update'] = agora
    return CACHE['noticias']

@app.route('/')
def inicio():
    noticias = pegar_noticias()
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True)
