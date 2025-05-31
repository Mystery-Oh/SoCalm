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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)