from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.
class MessageNotificateTestCase(TestCase):
    # test case to verify that a notification is created when a message is sent

    def setUp(self):
        # Set up test users
        self.user1 = User.objects.create_user(user_name='sender', password='pass1234')
        self.user2 = User.objects.create_user(user_name='receiver', password='pass1234')

    def test_notification_created_on_message_send(self):
        # Send a message from user1 to user2
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello!, this is a test message.')

        # Check that a notification is created for user2
        notification = Notification.objects.filter(user=self.user2, message=message).first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertIn(self.user1.username, notification.notification_text)
        self.assertFalse(notification.is_read)

    def test_no_notification_0n_message_update(self):
        # test that no additional notification is created when a message is updated
        message = Message.objects.create(
            sender = self.user1,
            receiver = self.user2,
            content = 'Original Message'
        )

        # Get initial notification count
        initial_count = Notification.objects.filter(user=self.user2).count()

        # Update the message content
        message.content = 'Updated Message'
        message.save()

        # Check that no new notification is created
        final_count = Notification.objects.filter(user=self.user2).count()
        self.assertEqual(initial_count, final_count)

    def test_multiple_messages_create_multiple_notifications(self):
        # test that multiple messages create multiple notifications
        for i in range(5):
            Message.objects.create(
                sender = self.user1,
                receiver = self.user2,
                content = f'Message {i+1}'
            )

        # Check that 5 notifications are created for user2
        notifications = Notification.objects.filter(user=self.user2)
        self.assertEqual(notifications.count(), 5)