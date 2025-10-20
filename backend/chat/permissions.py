from django.utils import timezone
from django.db.models import Q
from .models import Profile, Contact, Message
from channels.db import database_sync_to_async

@database_sync_to_async
def can_send_message(sender_user, receiver_id):
    try:
        sender_profile = Profile.objects.get(user=sender_user)
        receiver_profile = Profile.objects.select_related('user').get(user_id=receiver_id)
    except Profile.DoesNotExist:
        return False, "Invalid sender or receiver."

    # Rule 1: Official cannot contact another Official
    if sender_profile.role == Profile.Role.OFFICIAL and receiver_profile.role == Profile.Role.OFFICIAL:
        return False, "Officials cannot contact each other."

    # Rule 2: Player <-> Official
    if sender_profile.role != receiver_profile.role:
        contact_exists = Contact.objects.filter(
            (Q(user1=sender_user, user2=receiver_profile.user) |
             Q(user1=receiver_profile.user, user2=sender_user))
        ).exists()
        if not contact_exists:
            Contact.objects.create(user1=sender_user, user2=receiver_profile.user)
            
        if sender_profile.role == Profile.Role.PLAYER:
            today = timezone.now().date()
            messages_to_official_today = Message.objects.filter(
                sender=sender_user,
                receiver=receiver_profile.user,
                timestamp__date=today
            ).count()
            if messages_to_official_today >= 5:
                return False, "You have reached your daily limit of 5 messages to this official."

    # Rule 3: Daily limit for Player
    if sender_profile.role == Profile.Role.PLAYER:
        today = timezone.now().date()
        total_messages_today = Message.objects.filter(
            sender=sender_user,
            timestamp__date=today
        ).count()
        if total_messages_today >= 100:
            return False, "You have reached your daily limit of 100 messages."

    return True, None
