from flask import Flask, render_template
import feedparser
import time

app = Flask(__name__)

# Feeds
FEED_BRASIL = 'https://g1.globo.com/rss/g1/internacional/'
FEED_PORTUGAL = 'https://www.rtp.pt/noticias/rss/internacional'

# Cache
cache = {
    'brasil': {'noticias': [], 'ultima_atualizacao': 0},
    'portugal': {'noticias': [], 'ultima_atualizacao': 0}
}
INTERVALO_ATUALIZACAO = 600  # 10 minutos

def buscar_rss(url):
    feed = feedparser.parse(url)
    noticias = []
    for entrada in feed.entries:
        noticias.append({
            'titulo': entrada.title,
            'resumo': entrada.summary,
            'link': entrada.link,
            'imagem': entrada.get('media_content', [{'url': None}])[0]['url'] if 'media_content' in entrada else None
        })
    return noticias

@app.route('/')
def index():
    agora = time.time()

    # Atualiza feed do Brasil
    if agora - cache['brasil']['ultima_atualizacao'] > INTERVALO_ATUALIZACAO:
        cache['brasil']['noticias'] = buscar_rss(FEED_BRASIL)
        cache['brasil']['ultima_atualizacao'] = agora

    # Atualiza feed de Portugal
    if agora - cache['portugal']['ultima_atualizacao'] > INTERVALO_ATUALIZACAO:
        cache['portugal']['noticias'] = buscar_rss(FEED_PORTUGAL)
        cache['portugal']['ultima_atualizacao'] = agora

    return render_template(
        'index.html',
        noticias_brasil=cache['brasil']['noticias'],
        noticias_portugal=cache['portugal']['noticias']
    )

if __name__ == '__main__':
    app.run(debug=True)
