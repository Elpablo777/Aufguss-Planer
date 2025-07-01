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

    def validate(self, data):
        """
        Check that start_time is before end_time.
        """
        # Bei partiellen Updates (PATCH) sind start_time oder end_time möglicherweise nicht im Daten-Dictionary.
        # In diesem Fall holen wir sie aus der Instanz (wenn vorhanden).
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError({"end_time": "Endzeit muss nach der Startzeit liegen."})
        return data

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_name', 'content', 'timestamp']
