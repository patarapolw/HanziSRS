from flask import Flask, request, render_template, Markup
from subprocess import Popen

from analyze import Analysis
from analyze.lookup import SpoonFed


class WebContents:
    def __init__(self):
        self.user = Analysis()
        self.sentences = SpoonFed()

    def print_sentences(self, tags):
        def iter_sentence():
            for sen_content, sentence_tags in self.user.sentences:
                if all([(tag in sentence_tags) for tag in tags]):
                    yield sen_content

        html = ''
        for sentence in iter_sentence():
            html += "<a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a> {1}<br />"\
                .format(sentence, list(self.sentences.iter_lookup(sentence))[0]['English'])

        return html

    def print_vocabs(self, tags):
        def iter_vocab():
            for vocab, vocab_note in self.user.vocabs:
                if all([(tag in vocab_note['tags']) for tag in tags]):
                    yield vocab_note['fields']

        html = ''
        for fields in iter_vocab():
            html += "<a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a><br />" \
                    "{1}<br />"\
                .format(fields['Simplified'], fields['English'])
            for i, sentence_entry in enumerate(self.sentences.iter_lookup(fields['Simplified'])):
                if i >= 5:
                    break
                html += "<a href='#' onclick='$.post(\"/speak\", {{spoken: \"{0}\"}}); return false;'>{0}</a><br />"\
                        "{1}<br />"\
                    .format(sentence_entry['Chinese'], sentence_entry['English'])

        return html


app = Flask(__name__)
contents = WebContents()


@app.route("/")
def index():
    html = "<form action='/execute' method='POST'>" \
           "Tags: <input type='text' name='tags'><br />" \
           "Type: " \
           "<input type='radio' name='type' value='vocab'>Vocab" \
           "<input type='radio' name='type' value='sentences'>Sentences" \
           "<input type='submit' value='Submit'>" \
           "</form><br />"
    html += "Available tags: {}".format(repr(contents.user.tags))

    return render_template('index.html', content=Markup(html))


@app.route("/execute", methods=['POST'])
def execute():
    if request.method == 'POST':
        data = request.form
        tags = data['tags'].split(' ')
        if data['type'] == 'vocab':
            html = contents.print_vocabs(tags)
        else:
            html = contents.print_sentences(tags)
    else:
        html = ''

    return render_template('index.html', content=Markup(html))


@app.route("/speak", methods=['POST'])
def speak():
    if request.method == 'POST':
        Popen(['say', '-v', 'ting-ting', request.form['spoken']])
        return ''
    return ''


if __name__ == '__main__':
    app.run()
