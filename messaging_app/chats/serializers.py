from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles password properly for user registration.
    """
    password = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'created_at', 'full_name', 'password'
        ]
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender details."""
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for creating messages.
    """
    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'message_body']
    
    def validate(self, data):
        # Ensure sender is a participant in the conversation
        if data['sender'] not in data['conversation'].participants.all():
            raise serializers.ValidationError(
                "Sender must be a participant in the conversation."
            )
        return data


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with participants and messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for conversation list views."""
    participants = UserSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'message_count', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()