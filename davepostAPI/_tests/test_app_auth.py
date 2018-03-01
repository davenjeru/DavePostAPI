from flask_testing import TestCase

from davepostAPI import app
from davepostAPI.api.v1 import api_v1
from davepostAPI.api.v1.auth import Login
from davepostAPI.api.v1.auth import Register


class AppTestCase(TestCase):
    def create_app(self):
        app.testing = True
        return app

    def setUp(self):
        self.client = self.create_app().test_client()

    def tearDown(self):
        pass

    def test_base_index(self):
        rv = self.client.get('/')
        self.assert404(rv)

    def test_api_index(self):
        rv = self.client.get(api_v1.base_url)
        self.assert200(rv)

    def test_not_json(self):
        rv = self.client.post(api_v1.url_for(Register))
        self.assertEqual(415, rv.status_code)

    def test_no_data(self):
        rv = self.client.post(api_v1.url_for(Register), content_type='application/json')
        self.assertEqual(400, rv.status_code)
        self.assertIn(b'no data was found in the request', rv.data)

    def register(self, email: str = None, password_tuple: tuple = (None, None), security_tuple: tuple = (None, None)):
        data = dict(email=email)
        data['password'], data['confirm_password'] = password_tuple
        data['security_question'], data['security_answer'] = security_tuple
        return self.client.post(api_v1.url_for(Register), data=str(data), content_type='application/json')

    def test_a1_register_pass(self):
        password_tuple = ('password.Pa55word', 'password.Pa55word')
        security_tuple = ('What is your favourite company?', 'company')

        rv = self.register('email@company.com', password_tuple, security_tuple)
        self.assertEqual(201, rv.status_code)
        self.assertIn(b'user registered successfully', rv.data)
        rv = self.register('email@company.com', password_tuple, security_tuple)
        self.assertIn(b'user with similar email exists', rv.data)
        self.assert400(rv)

    def test_a2_register_missing_parameter(self):
        rv = self.register('email@company.com')
        self.assert400(rv)
        self.assertIn(b'missing', rv.data)

    def test_a3_register_invalid_password(self):
        password_tuple = ('password', 'password')
        security_tuple = ('What is your favourite company?', 'company')
        rv = self.register('email@company.com', password_tuple, security_tuple)
        self.assert400(rv)
        self.assertIn(b'password syntax is invalid', rv.data)

    def test_a4_register_passwords_no_match(self):
        password_tuple = ('password.Pa55word', 'password')
        security_tuple = ('What is your favourite company?', 'company')
        rv = self.register('email@company.com', password_tuple, security_tuple)
        self.assert400(rv)
        self.assertIn(b'passwords do not match', rv.data)

    def login(self, email: str = None, password: str = None):
        data = dict(email=email, password=password)
        return self.client.post(api_v1.url_for(Login), data=str(data), content_type='application/json')

    def test_a7_login(self):
        email = 'email@company.com'
        password = 'password.Pa55word'
        rv = self.login(email, password)
        self.assert200(rv)
        self.assertIn(b'user logged in successfully', rv.data)

        rv = self.login(email, password)
        self.assert400(rv)
        self.assertIn(b'currently logged in', rv.data)

    def test_a8_login_fail(self):
        email = 'email@company.com'
        password = 'not.a.5imilaRpass'
        rv = self.login(email, password)
        self.assert401(rv)
        self.assertIn(b'invalid password', rv.data)

        email = 'email254@company.com'
        rv = self.login(email, password)
        self.assert400(rv)
        self.assertIn(b'user not found', rv.data)

        rv = self.login(None, password)
        self.assert400(rv)
        self.assertIn(b'missing', rv.data)
