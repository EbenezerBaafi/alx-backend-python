from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.sender == request.user


class IsParticipantInConversation(permissions.BasePermission):
    """
    Custom permission to check if user is a participant in the conversation.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is a participant in the conversation
        return request.user in obj.participants.all()


class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow message owners to edit/delete messages.
    """
    def has_object_permission(self, request, view, obj):
        # Only allow the message sender to modify the message
        return obj.sender == request.user


class CanAccessConversation(permissions.BasePermission):
    """
    Permission to check if user can access a conversation.
    Users can only access conversations they are participants in.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # User must be a participant in the conversation
        return request.user in obj.participants.all()