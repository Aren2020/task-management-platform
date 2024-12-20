from rest_framework.test import APITestCase
from datetime import datetime
from ..serializers import UserSerializer

class UserSerializerTest(APITestCase):
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

    def test_valid_data(self):
        serializer = UserSerializer(data = self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        serializer = UserSerializer(data = self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['username', 'email', 'first_name', 'last_name', 'password']))