from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def buscar_noticias():
    url = 'https://news.google.com/rss/search?q=tecnologia&hl=pt-PT&gl=PT&ceid=PT:pt'
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.content, 'xml')
    itens = soup.find_all('item')[:10]

    noticias = []
    for item in itens:
        titulo = item.title.text
        link = item.link.text
        descricao = item.description.text

        noticia = {
            'titulo': titulo,
            'link': link,
            'resumo': descricao,
            'imagem': 'https://source.unsplash.com/400x200/?technology'
        }
        noticias.append(noticia)

    return noticias

@app.route('/')
def home():
    noticias = buscar_noticias()
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
