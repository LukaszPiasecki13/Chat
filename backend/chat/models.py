from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.TextChoices):
        PLAYER = 'PLAYER', 'player'
        OFFICIAL = 'OFFICIAL', 'official'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Contact(models.Model):
    user1 = models.ForeignKey(User, related_name='contacts1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='contacts2', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_contact')
        ]

    def __str__(self):
        return f"{self.user1.username} <-> {self.user2.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']