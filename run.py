from flask import Flask, render_template, jsonify
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from dotenv import load_dotenv
import json


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

def run_api_call():
    print("호출 시작")
    subprocess.run(['python', 'Dataset/api_call.py'])
    print("api 호출됨")

@app.route('/run-api-call')
def manual_run():
    run_api_call()
    return "날씨 데이터 갱신 완료"

@app.route('/danger-data')
def danger_data():
    with open('algorithms/danger.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_api_call, 'interval', hours=1)
    scheduler.start()
    run_api_call()  # 앱 실행 즉시 수동으로 한번  실행
    app.run(host='0.0.0.0', debug=True, use_reloader=False)