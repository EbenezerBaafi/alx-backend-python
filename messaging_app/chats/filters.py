import django_filters
from .models import Message, Conversation
from django.db.models import Q

class MessageFilter(django_filters.FilterSet):
    # Filter by conversation ID
    conversation = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    
    # Filter by a specific sender's ID
    sender = django_filters.UUIDFilter(field_name='sender__user_id')
    
    # Filter by a datetime range (e.g., ?start_date=...&end_date=...)
    created_at_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'created_at_after', 'created_at_before']