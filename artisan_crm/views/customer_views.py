from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime

from ..models import CustomerProfile, Interaction, Lead, Tag

class CustomerListView(LoginRequiredMixin, ListView):
    model = CustomerProfile
    template_name = 'artisan_crm/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CustomerProfile.objects.using('artisan_crm').select_related().prefetch_related('interactions')
        
        # Filter by search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter by tags
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(customertag__tag__name=tag)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.using('artisan_crm').all()
        context['search'] = self.request.GET.get('search', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        return context

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = 'artisan_crm/customer_detail.html'
    context_object_name = 'customer'
    
    def get_object(self):
        return get_object_or_404(CustomerProfile.objects.using('artisan_crm'), pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        # Get interactions timeline
        interactions = customer.interactions.using('artisan_crm').order_by('-created_at')[:20]
        context['interactions'] = interactions
        
        # Get lead info if exists
        try:
            lead = Lead.objects.using('artisan_crm').get(customer=customer)
            context['lead'] = lead
        except Lead.DoesNotExist:
            context['lead'] = None
        
        # Get customer tags
        context['customer_tags'] = [ct.tag for ct in customer.customertag_set.using('artisan_crm').select_related('tag')]
        
        return context

@csrf_exempt
def generate_summary(request, customer_id):
    """Generate AI summary for customer"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    customer = get_object_or_404(CustomerProfile.objects.using('artisan_crm'), pk=customer_id)
    
    # Simple summary for now
    summary = f"Customer: {customer.name}, Source: {customer.source}"
    
    # Update customer summary
    customer.summary = summary
    customer.save(using='artisan_crm')
    
    return JsonResponse({'summary': summary})

@csrf_exempt
def suggest_reply(request, customer_id):
    """Generate AI reply suggestion"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    message_text = data.get('message', '')
    
    # Simple reply suggestion
    suggested_reply = f"Thank you for your message: {message_text[:50]}..."
    
    return JsonResponse({'reply': suggested_reply})

@csrf_exempt
def add_interaction(request, customer_id):
    """Add new interaction"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    customer = get_object_or_404(CustomerProfile.objects.using('artisan_crm'), pk=customer_id)
    
    interaction = Interaction.objects.using('artisan_crm').create(
        customer=customer,
        channel=data.get('channel', 'internal'),
        direction=data.get('direction', 'outbound'),
        content=data.get('content', '')
    )
    
    return JsonResponse({
        'id': interaction.id,
        'content': interaction.content,
        'channel': interaction.channel,
        'direction': interaction.direction,
        'created_at': interaction.created_at.isoformat()
    })