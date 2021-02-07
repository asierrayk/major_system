from flask import Flask, render_template, request
from major_system import AvailableDatabases, AvailableEncodeSystems
app = Flask(__name__)


@app.route('/')
def main():
    word = "main"
    return render_template("index.html", word=word)

@app.route('/encode/', methods=['GET'])
def encode():
    search = request.args.get("search")
    results = None
    search_method = "encode"
    if search is not None:
        database = "spanish"
        encoder = "mine"

        word_database = AvailableDatabases[database.upper()].value
        words = word_database.get_db()

        encoder = AvailableEncodeSystems[encoder.upper()].value

        encoded_words = encoder.encode(search, words)

        results = encoded_words.word.tolist()
    return render_template("search.html", search_method=search_method, results=results)

@app.route('/decode/')
def decode():
    word = "decode"
    return render_template("index.html", word=word)

@app.route('/configuration/')
def configuration():
    word = "configuration"
    return render_template("index.html", word=word)

if __name__ == '__main__':
    app.run()