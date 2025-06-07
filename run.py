from flask import Flask, render_template
import os
from dotenv import load_dotenv
import json
from flask import Flask, render_template, jsonify
from flask import Flask, render_template, request, jsonify



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

@app.route("/danger-data")
def danger_data():
    with open("algorithms/danger_fixed.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)