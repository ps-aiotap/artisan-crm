from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import os

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        identity_url = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001/api/')
        app_name = os.environ.get('APP_NAME', 'artisan_crm')
        
        try:
            response = requests.post(f'{identity_url}auth/login/', json={
                'username': username,
                'password': password,
                'app_name': app_name
            })
            
            if response.status_code == 200:
                user_data = response.json()
                request.session['at_identity_user_id'] = user_data['id']
                return redirect('/crm/')
            else:
                messages.error(request, 'Invalid credentials')
        except:
            messages.error(request, 'Authentication service unavailable')
    
    return render(request, 'artisan_crm/login.html')

def logout_view(request):
    request.session.pop('at_identity_user_id', None)
    return redirect('/')

def sync_user_to_identity(user_data):
    identity_url = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001/api/')
    app_name = os.environ.get('APP_NAME', 'artisan_crm')
    
    response = requests.post(f'{identity_url}sync/user/', json={
        'app_name': app_name,
        'user_data': {
            'username': user_data['username'],
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
        }
    })
    return response.json()

def user_has_permission(external_user_id, permission):
    identity_url = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001/api/')
    app_name = os.environ.get('APP_NAME', 'artisan_crm')
    
    response = requests.post(f'{identity_url}verify-permission/', json={
        'app_name': app_name,
        'external_user_id': external_user_id,
        'permission': permission
    })
    return response.json().get('has_permission', False)