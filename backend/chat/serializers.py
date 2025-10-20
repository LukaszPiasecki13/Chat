# backend/chat/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Message

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True) 

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'content', 'timestamp']
        read_only_fields = ['sender', 'receiver', 'timestamp']

    def validate_receiver_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with this ID does not exist.")
        return value