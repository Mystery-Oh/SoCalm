import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client() # 테스트용 클라이언트 생성
        self.app.testing = True

    def test_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('로그인'.encode('utf-8'), response.data)  # html에 '로그인'이라는 글자가 있는지

    def test_signup_page(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.app.get('/homepage')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()