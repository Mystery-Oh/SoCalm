import unittest
import sys
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_DIR = os.path.join(BASE_DIR, 'SoCalm_Project')
sys.path.insert(0, PROJECT_DIR)

from run import app, User, db

load_dotenv(os.path.join(BASE_DIR, '.env'))

class FlaskTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # 인메모리 DB
        self.app = app
        self.client = app.test_client()

        with self.app.app_context(): #db에다 테스트 유저넣기
            db.create_all()
            user = User(name='테스트유저', username='testuser')
            user.set_password('correct_password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_login_page_loads(self):
        with self.client.session_transaction() as sess:
            sess.clear()  # 세션 비우기
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)  # 유니코드 문자열(str)로 변환
        self.assertIn('Sign in', text)

    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        with self.client.session_transaction() as session:
            session.clear() #로그인 안한상태로 세션 초기화

        response = self.client.get('/homepage')
        self.assertEqual(response.status_code, 302) #로그인 안했을때, /login으로 리다이렉트

    def test_login_success(self):
        with self.client as c:
            response = c.post('/login', data={'username': 'testuser', 'password': 'correct_password'},
                              follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            with c.session_transaction() as sess:
                self.assertIn('user_id', sess)
                self.assertEqual(sess['username'], 'testuser')


    def test_signup_password_mismatch(self): #회원가입 실패 테스트
        response = self.client.post('/signup', data={
            'name': '홍길동',
            'username': 'hong',
            'password': '1234',
            'confirm_password': '5678'
        }, follow_redirects=True)
        text = response.get_data(as_text=True)  # 유니코드 문자열(str)로 변환
        self.assertIn('비밀번호가 일치하지 않습니다.', text)

    def test_logout(self):
        # 먼저 로그인 상태를 시뮬레이션
        with self.client.session_transaction() as session:
            session['user_id'] = 1
            session['username'] = 'testuser'

        # 실제로 logout 호출
        response = self.client.post('/logout', follow_redirects=True)

        # 세션이 비어야 함
        with self.client.session_transaction() as session:
            self.assertNotIn('user_id', session)
            self.assertNotIn('username', session)

        # 응답이 login 페이지로 redirect 됐는지 확인
        self.assertEqual(response.status_code, 200)  # follow_redirects=True로 썼으니 최종 응답은 200
        text = response.get_data(as_text=True)  # 유니코드 문자열(str)로 변환
        self.assertIn('Sign in', text)  # login_page에서 '로그인' 문구 있는지 확인

    def test_danger_data_json(self):
        response = self.client.get('/danger-data')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)

    def test_report_success(self):
        # 먼저 로그인 상태를 시뮬레이션
        with self.client.session_transaction() as session:
            session['user_id'] = 1
            session['username'] = 'testuser'

        # 올바른 데이터 보내기
        payload = {
            'lat': 37.5665,
            'lon': 126.9780,
            'location': '서울 시청',
            'description': '도로 파손'
        }

        response = self.client.post('/report', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('제보가 성공적으로 접수되었습니다.', data['message'])


if __name__ == '__main__':
    unittest.main()