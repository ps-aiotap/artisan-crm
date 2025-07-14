from django.urls import path
from .views import customer_views, pipeline_views
from . import auth_views

app_name = 'artisan_crm'

urlpatterns = [
    # Authentication
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Customer views
    path('', customer_views.CustomerListView.as_view(), name='customer_list'),
    path('customers/', customer_views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', customer_views.CustomerDetailView.as_view(), name='customer_detail'),
    
    # AI endpoints
    path('customers/<int:customer_id>/summary/', customer_views.generate_summary, name='generate_summary'),
    path('customers/<int:customer_id>/reply/', customer_views.suggest_reply, name='suggest_reply'),
    path('customers/<int:customer_id>/interaction/', customer_views.add_interaction, name='add_interaction'),
    
    # Pipeline views
    path('pipeline/', pipeline_views.LeadPipelineView.as_view(), name='pipeline'),
    path('pipeline/move/', pipeline_views.move_lead, name='move_lead'),
]