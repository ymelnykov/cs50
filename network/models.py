from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True, related_name="followers")
    following = models.ManyToManyField('self', blank=True, related_name="following")

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return f'Post {self.id} made by {self.poster} on {self.timestamp.strftime("%d/%m/%y %H:%M:%S")}'
