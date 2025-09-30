from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification



@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
      """
    Signal handler that automatically creates a notification when a new message is created.
    
    Args:
        sender: The model class (Message)
        instance: The actual message instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    # Check if a new message was created
      if created:
        # Create a notification for the recipient of the message
        notification_text = f" You have a new message from {instance.sender.username}"

        # create the notification for the user
        Notification.objects.create(
            user = instance.receiver,
            message = instance,
            notification_text = notification_text,
            is_read = False
        )

        print(f"Notification created for {instance.receiver.username}")

# signal to mark message as read when notification is read
@receiver(post_save, sender=Notification)
def mark_message_as_read(sender, instance, created, **kwargs):
    """
    Signal handler that marks the associated message as read when the notification is marked as read.
    
    Args:
        sender: The model class (Notification)
        instance: The actual notification instance that was saved
        **kwargs: Additional keyword arguments
    """
    # Check if the notification is marked as read
    if not created and instance.is_read:
        # find all notifications related to the same message
        notifications = Notification.objects.filter(message=instance, is_read=False)

        # mark all related notifications as read
        notifications.update(is_read=True)