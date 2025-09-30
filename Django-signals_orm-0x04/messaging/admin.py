from django.contrib import admin
from .models import Message, Notification

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for the Message model."""
    list_display = ('sender', 'receiver','content_preview' 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read', 'timestamp')
    readonly_fields = ['timestamp',]
    date_hierarchy = 'timestamp'

    def content_preview(self, obj):
        """Returns a preview of the message content."""
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model.
    """
    list_display = ['user', 'notification_text', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'notification_text']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Action to mark selected notifications as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        """Action to mark selected notifications as unread."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    
    mark_as_unread.short_description = 'Mark selected notifications as unread'