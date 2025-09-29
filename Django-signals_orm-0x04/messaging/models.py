from django.db import models
from django.contrib.auth.models import User


# Model to store messages between users
class Message():
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'Message from {self.sender.username} to {self.reciever.username} at {self.timestamp}'
    

# Model to store notifications for users
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(Message, on_delete=models.CASCADE, related_name='notifications')
    notification_text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f'Notification for {self.user.username} at {self.timestamp}'
    
    # Method to mark notification as read
    def mark_as_read(self):
        self.is_read = True
        self.save()
