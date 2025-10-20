from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Message
from .serializers import UserSerializer, MessageSerializer

class UserListView(generics.ListAPIView):
    """ Returns a list of all users except the logged-in user. """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id).prefetch_related('profile')
    
class UserDetailView(generics.RetrieveAPIView):
    """ Returns details of a specific user by ID. """
    queryset = User.objects.all().prefetch_related('profile')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ConversationListView(generics.ListAPIView):
    """ Returns the conversation (messages) between the logged-in user and another user. """
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        other_user_id = self.kwargs['user_id']
        user = self.request.user

        return Message.objects.filter(
            (Q(sender=user, receiver_id=other_user_id) |
             Q(sender_id=other_user_id, receiver=user))
        ).select_related('sender', 'receiver')