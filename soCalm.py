from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def homepage():

    tmap_api_key = os.environ.get('TMAP_API_KEY')

    return render_template('homepage.html')

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)