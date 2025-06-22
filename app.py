from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re

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
        descricao_html = item.description.text

        # Remove todas as tags HTML da descrição
        descricao_limpa = re.sub('<[^<]+?>', '', descricao_html)

        noticia = {
            'titulo': titulo,
            'link': link,
            'descricao': descricao_limpa,
            'imagem': f'https://source.unsplash.com/400x200/?technology,news,{titulo}',
            'fonte': 'Google News'
        }
        noticias.append(noticia)

    return noticias

@app.route('/')
def home():
    noticias = buscar_noticias()
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(debug=True)
