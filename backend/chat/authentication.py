# backend/chat/authentication.py
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework import exceptions

class XUserIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return None 
        try:
            user = User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)
