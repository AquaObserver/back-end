# Generated by Django 4.2.7 on 2023-12-15 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AquaObserver_api', '0002_userthreshold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userthreshold',
            name='userId',
        ),
    ]
