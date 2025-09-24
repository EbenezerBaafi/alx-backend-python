from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages within it.
    """
    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For a message object, check if the user is a participant of the message's conversation
        if isinstance(obj, Message):
            conversation = obj.conversation
            is_participant = request.user in conversation.participants.all()
            if is_participant:
                # Allow all safe methods (GET, HEAD, OPTIONS) for participants
                if request.method in permissions.SAFE_METHODS:
                    return True
                # Allow unsafe methods (PUT, PATCH, DELETE) only if the user is the message sender
                else:
                    return obj.sender == request.user
            return False
        
        # For a conversation object, check if the user is a participant
        elif isinstance(obj, Conversation):
            return request.user in obj.participants.all()
            
        return False