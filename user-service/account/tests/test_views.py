from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class RegistrationTest(APITestCase):
    
    def setUp(self):
        self.valid_data = {
            'username': 'Ryan1980',
            'email': 'ryangosling@gmail.com',
            'first_name': 'Ryan',
            'last_name': 'Gosling',
            'password': '********',
        }

        self.invalid_data = {
            'email': 'mail.com',
            'first_name': False,
            'last_name': datetime(day = 12, month = 11, year = 1980),
        }
        self.url = reverse('signup')

    def test_valid_data(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username = self.valid_data['username']).exists())
        self.assertEqual(set(response.data), set(['access', 'refresh']))

    def test_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTest(APITestCase):
    
    def setUp(self):
        User.objects.create_user(
            username = 'Lolo',
            email = 'ryangosling@gmail.com',
            first_name =  'Ryan',
            last_name = 'Gosling',
            password = 'Lolo2020',
        )
        self.valid_user = {
            'username': 'Lolo',
            'password': 'Lolo2020'
        }
        self.invalid_user = {
            'username': 'Rho',
            'password': '********'
        }

        self.login_url = reverse('login')
    
    def test_valid_user(self):
        response = self.client.post(self.login_url, self.valid_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), set(['refresh', 'access']))
    
    def test_invalid_user(self):
        response = self.client.post(self.login_url, self.invalid_user)
        self.assertEqual(response.status_code, 401)
    
    def test_no_data(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 400)
    
class LogoutTest(APITestCase):
    
    def setUp(self):
        User.objects.create_user(
            username = 'Ryan1980',
            email = 'ryangosling@gmail.com',
            first_name =  'Ryan',
            last_name = 'Gosling',
            password = '********',
        )

        self.valid_token = self.client.post(reverse('login'),
            {
               'username': 'Ryan1980',
               'password': '********'
            }
        ).data.get('refresh')
        self.invalid_token = 'sdfdsfs'

        self.logout_url = reverse('logout')

    def test_valid_token(self):
        response = self.client.post(self.logout_url, {'refresh_token': self.valid_token})
        self.assertEqual(response.status_code, 200)

    def test_invalid_token(self):
        response = self.client.post(self.logout_url, {'refresh_token': self.invalid_token})
        self.assertEqual(response.status_code, 400)

    def test_no_token(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 400)
    
    