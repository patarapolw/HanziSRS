from flask import Flask, request, render_template, Markup
from subprocess import Popen
from bs4 import BeautifulSoup
from random import shuffle
import jieba
import json

from analyze import Analysis
from analyze.lookup import SpoonFed, HanziVariant, Cedict
from analyze.api import jukuu


class WebContents:
    def __init__(self):
        self.user = Analysis()
        self.sentences = SpoonFed()
        self.hanzi_variant = HanziVariant()
        self.cedict = Cedict()

    def print_sentences(self, tags):
        def iter_sentence():
            if 'random' in tags:
                entry_list = self.user.sentences
                shuffle(entry_list)
                for i, sentence_pair in enumerate(entry_list):
                    if i < 10:
                        yield sentence_pair[0]
            for sen_content, sentence_tags in self.user.sentences:
                if all([(tag in sentence_tags) for tag in tags]):
                    yield sen_content

        html = ''
        for sentence in iter_sentence():
            try:
                english = next(self.sentences.iter_lookup(sentence))['English']
            except StopIteration:
                english = ''
            html += "<a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a> {1}<br />"\
                .format(sentence, english)
            html += "<ul>"
            for word in jieba.cut(sentence):
                html += "<li><a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a>" \
                        " {1}</li>".format(word, self.cedict.get(word).get('english', ''))
            html += "</ul>"

        return html

    def print_vocabs(self, tags):
        def iter_vocab():
            if 'random' in tags:
                entry_list = self.user.vocabs
                shuffle(entry_list)
                for i, vocab_pair in enumerate(entry_list):
                    if i < 10:
                        yield vocab_pair[1]['fields']
            for vocab, vocab_note in self.user.vocabs:
                if all([(tag in vocab_note['tags']) for tag in tags]):
                    yield vocab_note['fields']

        html = ''
        for fields in iter_vocab():
            html += "<a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a><br />" \
                    "{1}<br /><ul>"\
                .format(fields['Simplified'], fields['English'])
            local_sentence = self.sentences.iter_lookup(fields['Simplified'])
            online_sentence = jukuu(fields['Simplified'])
            for i in range(5):
                try:
                    sentence_entry = next(local_sentence)
                except StopIteration:
                    try:
                        sentence_entry = next(online_sentence)
                    except StopIteration:
                        break
                html += "<li><a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a>"\
                        "{1}</li>"\
                    .format(sentence_entry['Chinese'], sentence_entry['English'])
            html += "</ul>"

        return html

    def print_hanzi(self, tags):
        def iter_hanzi():
            if 'random' in tags:
                entry_list = self.user.hanzi
                shuffle(entry_list)
                for i, hanzi_pair in enumerate(entry_list):
                    if i < 10:
                        yield hanzi_pair[0]
            for hanzi, hanzi_tags in self.user.hanzi:
                if all([(tag in hanzi_tags) for tag in tags]):
                    yield hanzi

        html = ''
        for hanzi in iter_hanzi():
            html += '<font style="font-size: 200px">{}</font><br />'.format(hanzi)
            html += self.hanzi_variant.get(hanzi) + '<br />'
            local_sentence = self.sentences.iter_lookup(hanzi)
            online_sentence = jukuu(hanzi)
            for i in range(5):
                try:
                    sentence_entry = next(local_sentence)
                except StopIteration:
                    try:
                        sentence_entry = next(online_sentence)
                    except StopIteration:
                        break
                html += "<li><a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a>" \
                        "{1}</li>" \
                    .format(sentence_entry['Chinese'], sentence_entry['English'])
            html += "</ul>"

        return html

    def print_tags(self):
        html = ''
        tags = ['random']
        tags.extend(sorted(set(self.user.tags)))
        for tag in tags:
            html += "<a href='#' onclick='appendToTags(\"{0}\"); return false'>{0}</a>, ".format(tag)

        html += "<script>function appendToTags(tag){" \
                "$('#tags').val(tag)}</script>"

        return html


app = Flask(__name__)
contents = WebContents()


@app.route("/")
def index():
    return render_template('main.html', tags=Analysis().tags)


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
