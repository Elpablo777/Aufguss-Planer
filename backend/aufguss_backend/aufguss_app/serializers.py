from rest_framework import serializers
from .models import SaunaUser, AufgussSession, ChatMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaunaUser
        fields = ['id', 'user', 'color', 'avatar', 'is_active', 'is_permanent_admin', 'full_name', 'created_at', 'updated_at']

class AufgussSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.full_name', read_only=True)
    created_by_color = serializers.CharField(source='created_by.color', read_only=True)
    class Meta:
        model = AufgussSession
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created_by', 'created_by_username', 'created_by_color', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_name', 'content', 'timestamp']
