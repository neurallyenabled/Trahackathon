from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
import unicodedata
import unicodedata
import idna
from email_validator import validate_email, EmailNotValidError
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def parse_mail(mail):
  mail_local, mail_domain = mail.split('@')
  mail_normal = unicodedata.normalize('NFC', mail_domain)
  mail_mail = '@'.join((mail_local, idna.encode(mail_normal).decode("ascii")))
  return mail_mail


@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))

    def __init__(self, long, short):
        self.long = long
        self.short = short

def shorten_url():
    letters = "أبتثجحخدذرزسشصضطظعغفقكلمنهوي١٢٣٤٥٦٧٨٩"
    while True:
        rand_letters = random.choices(letters, k=6)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        try:
            middle_url = url_received.split("https://")[1].split("/")[0]
            rest_link = url_received.split("https://")[1].split("/")[1:]
            extention = ""
            for i in rest_link:
                extention = extention+"/"+i
                
            normalized_input = unicodedata.normalize('NFC',middle_url)
            url_received = "https://"+normalized_input+extention
        except:
            url_received = request.form["nm"]
            url_received = url_received.split("https://")[1]
            normalized_input = unicodedata.normalize('NFC',url_received)
            url_received = "https://"+normalized_input
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

@app.route('/all_urls')
def display_all():
    return render_template('all_urls.html', vals=Urls.query.all())

# @app.route('email', methods=['POST'])
# def sendEmail():
#     email = request.form['email']
#     short_url = request.form['short_url']
#     print(email, short_url)

