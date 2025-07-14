"""
Artisan CRM settings for AT Identity integration
Add this to your main settings.py or import from here
"""

import os

# AT Identity Configuration
USE_AT_IDENTITY = os.environ.get('USE_AT_IDENTITY', 'True').lower() == 'true'
AT_IDENTITY_URL = os.environ.get('AT_IDENTITY_URL', 'http://localhost:8001/api/')
AT_IDENTITY_API_KEY = os.environ.get('AT_IDENTITY_API_KEY', 'your-api-key')
APP_NAME = os.environ.get('APP_NAME', 'artisan_crm')

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'artisan_crm.middleware.ATIdentityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Login/Logout URLs
LOGIN_URL = os.environ.get('LOGIN_URL', '/crm/login/')
LOGOUT_URL = os.environ.get('LOGOUT_URL', '/crm/logout/')
LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL', '/crm/')
LOGOUT_REDIRECT_URL = os.environ.get('LOGOUT_REDIRECT_URL', '/')