# backend/chat/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import Profile, Contact, Message

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Message.objects.all().delete()
        Contact.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating new data...')

        # Users
        player1 = User.objects.create_user(username='Zawodnik 1', password='password')
        player2 = User.objects.create_user(username='Zawodnik 2', password='password')
        official1 = User.objects.create_user(username='Działacz 1', password='password')
        official2 = User.objects.create_user(username='Działacz 2', password='password') 

        # Profiles
        Profile.objects.create(user=player1, role=Profile.Role.PLAYER)
        Profile.objects.create(user=player2, role=Profile.Role.PLAYER)
        Profile.objects.create(user=official1, role=Profile.Role.OFFICIAL)
        Profile.objects.create(user=official2, role=Profile.Role.OFFICIAL)

        # Contacts
        # Player 1 and Official 1 have exchanged contacts
        Contact.objects.create(user1=player1, user2=official1)

        # Messages
        Message.objects.create(sender=player1, receiver=player2, content='Hi, how’s it going?')
        Message.objects.create(sender=player2, receiver=player1, content='I’m good, thanks! How about you?')
        Message.objects.create(sender=player1, receiver=official1, content='Good morning, I have a question about the training.')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))
        self.stdout.write(self.style.SUCCESS(f'User IDs: Player 1: {player1.id}, Player 2: {player2.id}, Official 1: {official1.id}'))
