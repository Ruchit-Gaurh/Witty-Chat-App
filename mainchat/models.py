from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pic = models.CharField(max_length=1000, blank=True, null=True)
    friends = models.ManyToManyField('Friend', related_name="my_friends")

    def __str__(self):
        return self.name
    

class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.name


class ChatMessage(models.Model):
    body = models.TextField()
    msgsender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msgreciver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_reciver")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body