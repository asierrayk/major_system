from flask import Flask, render_template, request
from major_system import AvailableDatabases, AvailableEncodeSystems
import pandas as pd
app = Flask(__name__)


@app.route('/')
def main():
    word = "main"
    return render_template("index.html", word=word)

@app.route('/encode/', methods=['GET'])
def encode():
    search = request.args.get("search")
    dbs = request.args.getlist("db")
    encoder = request.args.getlist("encoder")
    results = None
    search_method = "encode"
    available_dbs = [db.name for db in AvailableDatabases]
    if search is not None:
        encoder = "mine"

        words_dbs = []
        for db in dbs:
            word_database = AvailableDatabases[db.upper()].value
            words_db = word_database.get_db()
            words_db["source"] = db
            words_dbs.append(words_db)

        words = pd.concat(words_dbs)
        encoder = AvailableEncodeSystems[encoder.upper()].value

        encoded_words = encoder.encode(search, words)

        results = encoded_words.word.tolist()
    return render_template("search.html", available_dbs=available_dbs, search_method=search_method, results=results)

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