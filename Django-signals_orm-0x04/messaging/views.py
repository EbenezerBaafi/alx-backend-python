from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, Notification
# Create your views here.

@login_required
def message_detail(request, message_id):
    """View to display a specific message and mark it as read."""
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    
    # Mark related notification as read
    Notification.objects.filter(user=request.user, message=message).update(is_read=True)
    
    return render(request, 'messaging/message_detail.html', {'message': message})

    # user.delete(), delete_user
    #Message.objects.filter", "delete()