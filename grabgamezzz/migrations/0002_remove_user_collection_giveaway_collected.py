# Generated by Django 4.1.1 on 2023-01-04 11:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabgamezzz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='collection',
        ),
        migrations.AddField(
            model_name='giveaway',
            name='collected',
            field=models.ManyToManyField(blank=True, related_name='collectors', to=settings.AUTH_USER_MODEL),
        ),
    ]
