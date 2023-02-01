from django.contrib import admin
from .models import User, Giveaway, Lastchecked

# Register your models here.
admin.site.register(User)
admin.site.register(Giveaway)
admin.site.register(Lastchecked)
