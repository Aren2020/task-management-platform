import requests
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

def user_data(request):
    response = requests.get(
        settings.USER_DATA_URL,
        headers = {
            'Authorization': request.headers['Authorization']
        }
    )
    
    if response.status_code != 200:
        raise AuthenticationFailed()
    return response.json()