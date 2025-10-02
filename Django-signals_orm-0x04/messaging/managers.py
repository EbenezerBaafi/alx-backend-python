from django.db import models

class UnreadMessagesManager(models.Manager):
    """Custom manager for handling unread messages."""
    
    def unread_for_user(self, user):
        """
        Get all unread messages for a specific user.
        
        Args:
            user: The user to get unread messages for
            
        Returns:
            QuerySet of unread messages optimized with select_related and only
        """
        return self.filter(
            receiver=user,
            is_read=False
        ).select_related('sender').only(
            'sender__username',
            'content', 
            'timestamp',
            'is_read'
        )