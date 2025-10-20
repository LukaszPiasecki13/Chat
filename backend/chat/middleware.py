# backend/chat/middleware.py
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

class UserSwitchMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.headers.get('X-User-ID')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                request.user = user
            except User.DoesNotExist:
                pass