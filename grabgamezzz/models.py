from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

# Create your models here.
class User(AbstractUser):

    def __str__(self):
        return self.username.capitalize()


class Giveaway(models.Model):
    title=models.CharField(max_length=128)
    image=models.URLField()
    description=models.TextField(max_length=2048)
    instructions=models.TextField(max_length=512)
    type=models.CharField(max_length=20)
    platforms=models.CharField(max_length=128)
    worth=models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    url=models.URLField()
    collected=models.ManyToManyField(User, blank=True, related_name='collectors')
    published_date=models.DateTimeField(default=timezone.now)
    expiry_date=models.DateField(blank=True, null=True)
    gp_id=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class Lastchecked(models.Model):
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


