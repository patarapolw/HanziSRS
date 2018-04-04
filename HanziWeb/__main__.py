from flask import Flask, request, render_template, Markup
from subprocess import Popen
from bs4 import BeautifulSoup
from random import shuffle
import jieba

from analyze import Analysis
from analyze.lookup import SpoonFed, HanziVariant, Cedict
from analyze.api import jukuu

app = Flask(__name__)
analysis = Analysis()
sentences = SpoonFed()
hanzi_variant = HanziVariant()
cedict = Cedict()


@app.route("/")
def index():
    return render_template('index.html', tags=analysis.tags)


@app.route("/execute", methods=['POST'])
def execute():
    if request.method == 'POST':
        data = request.form
        tags = data['tags'].strip().split(' ')
        if data['type'] == 'vocab':
            html = contents.print_vocabs(tags)
        elif data['type'] == 'hanzi':
            html = contents.print_hanzi(tags)
        else:
            html = contents.print_sentences(tags)
    else:
        html = ''

    return render_template('index.html', content=Markup(html))


@app.route("/speak", methods=['POST'])
def speak():
    if request.method == 'POST':
        Popen(['say', '-v', 'ting-ting', BeautifulSoup(request.form['spoken'], 'html.parser').text])
        return ''
    return ''


if __name__ == '__main__':
    app.run()
