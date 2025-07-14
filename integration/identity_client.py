"""
Artisan CRM integration with AT Identity service
"""
import requests
from typing import Dict, List, Optional
from django.conf import settings
from django.contrib.auth.models import User

class CRMIdentityClient:
    """Client for Artisan CRM to communicate with AT Identity service"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
        self.api_key = getattr(settings, 'AT_IDENTITY_API_KEY', '')
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def sync_user(self, user: User) -> bool:
        """Sync CRM user to AT Identity"""
        try:
            response = self.session.post(f'{self.base_url}sync/user/', json={
                'app_name': 'artisan',
                'user_data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_user_permissions(self, user: User) -> List[str]:
        """Get user CRM permissions from AT Identity"""
        try:
            response = self.session.get(
                f'{self.base_url}permissions/',
                params={
                    'app_name': 'artisan',
                    'external_user_id': user.id
                }
            )
            if response.status_code == 200:
                return response.json().get('permissions', [])
        except requests.RequestException:
            pass
        return []
    
    def has_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific CRM permission"""
        try:
            response = self.session.post(f'{self.base_url}verify-permission/', json={
                'app_name': 'artisan',
                'external_user_id': user.id,
                'permission': permission
            })
            if response.status_code == 200:
                return response.json().get('has_permission', False)
        except requests.RequestException:
            pass
        return False

# Global instance
crm_identity_client = CRMIdentityClient()