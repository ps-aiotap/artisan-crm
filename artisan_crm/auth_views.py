from django.shortcuts import render, redirect
from django.contrib import messages
import os
import requests

def login_view(request):
    """Handle login - try AT Identity first, fallback to simple auth"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try AT Identity if available
        identity_url = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001')
        try:
            response = requests.post(f'{identity_url}/api/auth/login/', json={
                'username': username,
                'password': password,
                'app_name': os.environ.get('APP_NAME', 'artisan')
            }, timeout=2)
            
            if response.status_code == 200:
                user_data = response.json()
                request.session['at_identity_user_id'] = user_data['id']
                return redirect('/crm/')
        except:
            pass
        
        # Fallback: simple demo authentication
        if username == 'admin' and password == 'admin':
            request.session['demo_user'] = {'id': 1, 'username': 'admin'}
            return redirect('/crm/')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'artisan_crm/login.html')

def logout_view(request):
    """Clear session and redirect"""
    request.session.flush()
    return redirect('/crm/login/')