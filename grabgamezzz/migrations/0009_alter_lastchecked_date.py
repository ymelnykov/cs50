# Generated by Django 4.1.1 on 2023-01-08 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabgamezzz', '0008_alter_lastchecked_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastchecked',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]