from flask import Flask, render_template, abort
import feedparser
import time
import re  # Importação para limpar HTML

app = Flask(__name__)

# Cache para evitar recarregar os feeds a cada request
CACHE = {'noticias': [], 'desporto': [], 'update': 0}
INTERVAL = 1200  # 20 minutos

# Feeds
FEED_G1 = "https://g1.globo.com/rss/g1/"
FEED_DESPORTO = "https://desportonoticias.webnode.pt/rss/futebol-nacional-e-internacional.xml"

# Função para remover tags HTML do texto
def limpar_html(texto):
    return re.sub(r'<[^>]+>', '', texto)

# Carrega os feeds RSS
def carregar_feed(url, max_itens=8):
    feed = feedparser.parse(url)
    lista = []
    for entry in feed.entries[:max_itens]:
        lista.append({
            'titulo': entry.title,
            'resumo': limpar_html(entry.get('summary', ''))[:200] + '…',
            'conteudo': entry.get('summary', ''),
            'link': entry.link,
            'imagem': entry.get('media_content', [{}])[0].get('url', '')
        })
    return lista

# Página inicial
@app.route("/")
def index():
    agora = time.time()
    if agora - CACHE['update'] > INTERVAL:
        CACHE['noticias'] = carregar_feed(FEED_G1)
        CACHE['desporto'] = carregar_feed(FEED_DESPORTO)
        CACHE['update'] = agora
    return render_template("index.html",
                           noticias=CACHE['noticias'],
                           desporto=CACHE['desporto'])

# Página da notícia
@app.route("/noticia/<tipo>/<int:id>")
def ver_noticia(tipo, id):
    if tipo not in CACHE:
        abort(404)
    if id < 0 or id >= len(CACHE[tipo]):
        abort(404)
    noticia = CACHE[tipo][id]
    return render_template("noticia.html", noticia=noticia)

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)
