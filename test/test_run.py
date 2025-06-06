import unittest
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from run import app, db

load_dotenv()

class FlaskTests(unittest.TestCase):

    def setUp(self):
        app.conifg['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # 인메모리 DB
        self.app = app
        self.client = app.test_client()

        with self.app.app_context():
            db.create_all()

        """self.app = app.test_client() # 테스트용 클라이언트 생성
        self.app.testing = True"""

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('로그인', response.data)

    def test_signup_page(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.app.get('/homepage')
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_user(self):
        # 사전에 유저를 DB에 넣어둔 후
        response = self.post('/login', data={'username': 'testuser', 'password': 'correct_password'})
        assert response.status_code == 302  # redirect expected
        assert '환영합니다!' in response.data

    def test_signup_password_mismatch(self): #회원가입 실패 테스트
        response = self.post('/signup', data={
            'name': '홍길동',
            'username': 'hong',
            'password': '1234',
            'confirm_password': '5678'
        }, follow_redirects=True)
        assert '비밀번호가 일치하지 않습니다' in response.data

    def test_danger_data_json(self):
        response = self.get('/danger-data')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)


if __name__ == '__main__':
    unittest.main()