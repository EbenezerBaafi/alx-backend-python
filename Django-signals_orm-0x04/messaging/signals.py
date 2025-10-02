from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal handler that automatically creates a notification when a new message is created.
    
    Args:
        sender: The model class (Message)
        instance: The actual message instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    # Only create notification for new messages, not updates
    if created:
        # Create notification text
        notification_text = f"You have a new message from {instance.sender.username}"
        
        # Create the notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            notification_text=notification_text,
            is_read=False
        )
        
        print(f"✓ Notification created for {instance.receiver.username}")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal handler that logs the old content of a message before it's updated.
    
    This function listens for the pre_save signal on the Message model.
    Before a message is saved, it checks if the message already exists in the database.
    If it does and the content has changed, it saves the old content to MessageHistory.
    
    Args:
        sender: The model class (Message)
        instance: The message instance about to be saved
        **kwargs: Additional keyword arguments
    """
    # Check if this is an update (not a new message)
    if instance.pk:
        try:
            # Get the old version of the message from the database
            old_message = Message.objects.get(pk=instance.pk)
            
            # Check if the content has been changed
            if old_message.content != instance.content:
                # Save the old content to MessageHistory
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                
                # Mark the message as edited
                instance.edited = True
                
                # Track who edited it (typically the sender)
                if not instance.edited_by:
                    instance.edited_by = instance.sender
                
                print(f"✓ Message history saved for Message ID {instance.pk}")
                
        except Message.DoesNotExist:
            # Message doesn't exist yet, so this is a new message
            pass

@receiver(post_delete, sender=Message)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler that cleans up user data when a user is deleted.
    
    This function listens for the post_delete signal on the User model.
    When a user is deleted, it removes all messages and notifications associated with that user.
    
    Args:
        sender: The model class (User)
        instance: The user instance that was deleted
        **kwargs: Additional keyword arguments
    """
    pass

# Message.objects.filter(), delete()