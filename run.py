from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
import os
from dotenv import load_dotenv
from models import db, User

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("오류: DATABASE_URL 환경 변수가 .env 파일에 설정되지 않았습니다. MySQL 연결 문자열을 설정해주세요.")
if not app.config['SECRET_KEY']:
    raise ValueError("오류: SECRET_KEY 환경 변수가 .env 파일에 설정되지 않았습니다.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def login():

    return render_template('LogInPage.html')

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

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)