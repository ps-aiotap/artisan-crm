from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse

# Custom error handlers
def custom_404_view(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

handler404 = custom_404_view

def home_redirect(request):
    return redirect('/crm/')

def debug_partner(request):
    """Direct partner dashboard bypass"""
    return HttpResponse("<h1>Debug Partner Dashboard</h1><p>CRM System Active</p>")

urlpatterns = [
    # path('admin/', admin.site.urls),  # Removed for userless system
    path('debug-partner/', debug_partner, name='debug_partner'),

    path('crm/', include('artisan_crm.urls')),
    path('', home_redirect, name='home'),
]

# Serve static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)