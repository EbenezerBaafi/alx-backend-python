# chats/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, 
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer, 
    MessageCreateSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Provides CRUD operations for conversations.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'conversation_id'
    
    def get_queryset(self):
        # Only return conversations where the current user is a participant
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Automatically adds the current user as a participant.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create conversation
        conversation = serializer.save()
        
        # Add current user as participant if not already included
        if request.user not in conversation.participants.all():
            conversation.participants.add(request.user)
        
        # Return full conversation data
        response_serializer = ConversationSerializer(conversation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, conversation_id=None):
        """
        Add a participant to an existing conversation.
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response({'message': 'Participant added successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_participant(self, request, conversation_id=None):
        """
        Remove a participant from an existing conversation.
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.remove(user)
            return Response({'message': 'Participant removed successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Provides CRUD operations for messages.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'message_id'
    
    def get_queryset(self):
        # Only return messages from conversations where user is a participant
        user_conversations = Conversation.objects.filter(
            participants=self.request.user
        )
        return Message.objects.filter(
            conversation__in=user_conversations
        ).select_related('sender', 'conversation')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation.
        """
        # Set sender to current user
        request.data['sender'] = request.user.user_id
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.save()
        
        # Return full message data
        response_serializer = MessageSerializer(message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_conversation(self, request):
        """
        Get all messages for a specific conversation.
        Usage: /api/messages/by_conversation/?conversation_id=<uuid>
        """
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants=request.user
            )
            messages = self.get_queryset().filter(conversation=conversation)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or access denied'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, *args, **kwargs):
        """
        Override update to only allow message owner to edit.
        """
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only edit your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to only allow message owner to delete.
        """
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only delete your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    #filters 