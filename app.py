from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('LogInPage.html')


@app.route('/signup')
def signup():
    return render_template('Signup.html')


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')