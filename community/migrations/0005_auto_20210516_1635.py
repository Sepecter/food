# Generated by Django 3.1.2 on 2021-05-16 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20210516_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='stars',
        ),
        migrations.AddField(
            model_name='articlepost',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]
