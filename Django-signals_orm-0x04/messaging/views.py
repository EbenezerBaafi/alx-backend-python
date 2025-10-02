from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Notification
from django.db import models
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.

@login_required
def message_detail(request, message_id):
    """View to display a specific message and its replies."""
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                      .prefetch_related('replies__sender', 'replies__receiver'),
        models.Q(id=message_id) & (models.Q(receiver=request.user) | models.Q(sender=request.user))
    )
    
    if not message.is_read and message.receiver == request.user:
        message.is_read = True
        message.save()
        
        # Mark related notification as read
        Notification.objects.filter(user=request.user, message=message).update(is_read=True)
    
    # Get the entire conversation thread
    thread = message.get_thread().order_by('timestamp')
    
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'thread': thread
    })

@login_required
def reply_to_message(request, message_id):
    """View to handle replies to messages."""
    parent_message = get_object_or_404(Message, id=message_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            reply = Message.objects.create(
                sender=request.user,
                receiver=parent_message.sender if parent_message.sender != request.user else parent_message.receiver,
                content=content,
                parent_message=parent_message
            )
            return redirect('message_detail', message_id=reply.id)
    
    return redirect(to='message_detail', message_id=message_id) 

# Message.objects.filter()

@login_required
def delete_user(request):
    """View to handle user account deletion."""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Redirect to home or login page after deletion
    
    return render(request, 'messaging/delete_account.html')