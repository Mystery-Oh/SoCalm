import unittest
import sys
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SoCalm_Project'))

print(BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, '.env'))

sys.path.insert(0, BASE_DIR)

from run import app, User, db


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

    def test_user_creation(self):
        user = User(name='테스트유저', username='testuser')
        user.set_password('password123')
        self.assertEqual(user.name, '테스트유저')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))

    def test_password_hashing(self):
        user = User(name='name', username='username')
        user.set_password('mypassword')
        self.assertNotEqual(user.password_hash, 'mypassword')  # 평문이 아니어야 함
        self.assertTrue(user.check_password('mypassword'))
        self.assertFalse(user.check_password('wrongpassword'))

    def test_user_db_crud(self):
        with self.app.app_context():
            user = User(name='Test User', username='testuser2')
            user.set_password('mypassword')
            db.session.add(user)
            db.session.commit()

            found = User.query.filter_by(username='testuser2').first()
            self.assertIsNotNone(found)
            self.assertTrue(found.check_password('mypassword'))