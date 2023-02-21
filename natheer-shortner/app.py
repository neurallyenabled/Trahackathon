from flask import Flask, render_template, request
import idna
import unicodedata

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/مختصر/<short_link>')
def shortened(short_link):
    return f'Hit From Shortened! ({short_link})'

@app.route('/create', methods=['POST'])
def create():
    url = request.form['url']
    normalized_url = unicodedata.normalize('NFC', url)
    url_alabel = idna.encode(normalized_url).decode("ascii")
    print(url_alabel)

    return render_template('index.html')
