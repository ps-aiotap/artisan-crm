import requests
import os
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect

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
        self.is_staff = user_data.get('is_staff', False)
        self.is_superuser = user_data.get('is_superuser', False)

class ATIdentityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.identity_url = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001').rstrip('/')
        self.app_name = os.environ.get('APP_NAME', 'artisan')
    
    def __call__(self, request):
        # Handle callback from AT Identity
        if 'at_identity_user_id' in request.GET:
            request.session['at_identity_user_id'] = request.GET['at_identity_user_id']
            return redirect('/crm/')
        
        user_id = request.session.get('at_identity_user_id')
        demo_user = request.session.get('demo_user')
        
        if user_id:
            try:
                response = requests.get(f'{self.identity_url}/api/users/{user_id}/', timeout=2)
                if response.status_code == 200:
                    user_data = response.json()
                    request.user = ATIdentityUser(user_data)
                else:
                    request.user = AnonymousUser()
            except:
                request.user = AnonymousUser()
        elif demo_user:
            # Fallback demo user
            request.user = ATIdentityUser({
                'id': demo_user['id'],
                'username': demo_user['username'],
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_active': True
            })
        else:
            request.user = AnonymousUser()
        
        return self.get_response(request)