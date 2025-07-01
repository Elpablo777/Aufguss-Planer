from rest_framework import serializers
from .models import SaunaUser, AufgussSession, ChatMessage
from django.contrib.auth.models import User
from typing import Dict, Any, Optional # Hinzugefügt für Typ-Hints
import datetime # Hinzugefügt für datetime Typ-Hints

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaunaUser
        fields = ['id', 'user', 'color', 'avatar', 'is_active', 'is_permanent_admin', 'full_name', 'created_at', 'updated_at']

class AufgussSerializer(serializers.ModelSerializer):
    created_by_username: str = serializers.CharField(source='created_by.full_name', read_only=True)
    created_by_color: str = serializers.CharField(source='created_by.color', read_only=True)
    # Model fields like 'title', 'start_time' etc. get their types from the model usually,
    # but for clarity, especially if not using django-stubs:
    title: str = serializers.CharField(max_length=100)
    description: Optional[str] = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    start_time: datetime.datetime = serializers.DateTimeField()
    end_time: datetime.datetime = serializers.DateTimeField()
    # created_by is a PrimaryKeyRelatedField to SaunaUser, which serializes to SaunaUser.id (int)
    # created_at, updated_at are DateTimeFields

    class Meta:
        model = AufgussSession
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'created_by', 'created_by_username', 'created_by_color', 'created_at', 'updated_at']

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check that start_time is before end_time.
        """
        start_time_val: Optional[datetime.datetime] = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time_val: Optional[datetime.datetime] = data.get('end_time', getattr(self.instance, 'end_time', None))

        if start_time_val and end_time_val and start_time_val >= end_time_val:
            raise serializers.ValidationError({"end_time": "Endzeit muss nach der Startzeit liegen."})
        return data

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name: str = serializers.CharField(source='sender.full_name', read_only=True)
    content: str = serializers.CharField()
    # timestamp is DateTimeField

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_name', 'content', 'timestamp']
