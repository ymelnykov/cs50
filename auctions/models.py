from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidding_user")
    bid = models.FloatField()

    def __float__(self):
        return self.bid


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500, blank=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner_user")

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="commented_listing")
    text = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.author} comment on {self.listing}'



    


