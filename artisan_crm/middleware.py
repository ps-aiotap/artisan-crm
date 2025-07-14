import requests
import os
from django.contrib.auth.models import AnonymousUser

class ATIdentityUser:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.first_name = user_data.get('first_name', '')
        self.last_name = user_data.get('last_name', '')
        self.is_active = user_data.get('is_active', True)
        self.is_authenticated = True
        self.is_anonymous = False

class ATIdentityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.identity_url = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001/api/')
        self.app_name = os.environ.get('APP_NAME', 'artisan_crm')
    
    def __call__(self, request):
        user_id = request.session.get('at_identity_user_id')
        if user_id:
            try:
                response = requests.get(f'{self.identity_url}users/{user_id}/', timeout=2)
                if response.status_code == 200:
                    user_data = response.json()
                    request.user = ATIdentityUser(user_data)
                else:
                    request.user = AnonymousUser()
            except:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        
        return self.get_response(request)