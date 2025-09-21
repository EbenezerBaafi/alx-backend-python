from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Excludes password for security and includes computed fields.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'created_at', 'full_name'
        ]
        read_only_fields = ['user_id', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Includes sender details as nested data.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    Includes participants and messages as nested relationships.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids', 
            'messages', 'message_count', 'last_message', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.first()  # Due to ordering in model
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation
    
    def update(self, instance, validated_data):
        participant_ids = validated_data.pop('participant_ids', None)
        
        if participant_ids is not None:
            participants = User.objects.filter(user_id__in=participant_ids)
            instance.participants.set(participants)
        
        return super().update(instance, validated_data)


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing conversations without all messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'message_count', 
            'last_message', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'message_body': last_message.message_body[:100] + '...' if len(last_message.message_body) > 100 else last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.email
            }
        return None


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