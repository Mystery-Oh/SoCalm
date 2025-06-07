from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session, jsonify
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from dotenv import load_dotenv
from models import db, User, Report
import json

load_dotenv()

app = Flask(__name__)

TMAP_API_KEY = os.getenv('TMAP_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("오류: DATABASE_URL 환경 변수가 .env 파일에 설정되지 않았습니다.")
if not app.config['SECRET_KEY']:
    raise ValueError("오류: SECRET_KEY 환경 변수가 .env 파일에 설정되지 않았습니다.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def login_page():
    if 'user_id' in flask_session:
        return redirect(url_for('homepage'))
    return render_template('LogInPage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('아이디와 비밀번호를 모두 입력해주세요.', 'danger')
            return redirect(url_for('login_page'))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            flask_session['user_id'] = user.id
            flask_session['username'] = user.username
            flash(f'{user.username}님, 환영합니다!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'danger')
            return redirect(url_for('login_page'))

    if 'user_id' in flask_session:
        return redirect(url_for('homepage'))
    return render_template('LogInPage.html')

@app.route('/logout', methods=['POST'])
def logout():
    flask_session.clear()  
    return redirect(url_for('login_page')) 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([name, username, password, confirm_password]):
            flash('모든 필드를 입력해주세요.', 'danger')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.', 'danger')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('이미 사용 중인 아이디입니다.', 'warning')
            return redirect(url_for('signup'))

        new_user = User(name=name, username=username)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'회원가입 처리 중 오류가 발생했습니다: {str(e)}', 'danger')
            return redirect(url_for('signup'))

    return render_template('Signup.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if 'user_id' not in flask_session:
        return redirect(url_for('login_page'))
    return render_template('homepage.html', tmap_app_key=TMAP_API_KEY)

@app.route('/score')
def score():
    if 'user_id' not in flask_session:
        return redirect(url_for('login_page'))
    return render_template('Score.html')

def run_api_call():
    print("호출 시작")
    result = subprocess.run(['python', 'Dataset/api_call.py'])
    if result.returncode == 0:
        print("api 호출성공")
    else:
        print("api 요청에 실패했습니다. api 서버 오류일 수 있으니 잠시 뒤에 다시 시도해주세요.")
        """ retry = subprocess.run(['python', 'Dataset/api_call.py'])
        if retry == 0:
            print("재요청 성공")
        else:
            print("재요청 실패")
            """

@app.route('/run-api-call')
def manual_run():
    run_api_call()
    return "날씨 데이터 갱신 완료"

@app.route('/danger-data')
def danger_data():
    with open('algorithms/danger.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# 로그아웃 후 뒤로가기로 웹페이지 접근 방지용
@app.after_request
def add_no_cache_headers(response):
    if request.endpoint != 'static':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

@app.route('/report', methods=['POST'])
def report():
    # 로그인한 사용자인지 확인
    if 'user_id' not in flask_session:
        return jsonify({'status': 'error', 'message': '로그인이 필요합니다.'}), 401

    # 사용자가 보낸 제보 데이터 받기
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': '잘못된 요청입니다.'}), 400

    lat = data.get('lat')
    lon = data.get('lon')
    location = data.get('location')
    description = data.get('description')
    user_id = flask_session['user_id']

    if not all([lat, lon, location, description]):
        return jsonify({'status': 'error', 'message': '모든 필드를 입력해주세요.'}), 400

    # 데이터베이스에 저장
    try:
        new_report = Report(
            latitude=lat,
            longitude=lon,
            location=location,
            description=description,
            user_id=user_id
        )
        db.session.add(new_report)
        db.session.commit()
        return jsonify({'status': 'success', 'message': '제보가 성공적으로 접수되었습니다.'})
    except Exception as e:
        db.session.rollback()
        print(f"DB 저장 오류: {e}")
        return jsonify({'status': 'error', 'message': '제보 처리 중 오류가 발생했습니다.'}), 500

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_api_call, 'interval', hours=1)
    scheduler.start()
    run_api_call()  
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
