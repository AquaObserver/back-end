# Generated by Django 4.2.7 on 2023-12-06 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AquaObserver_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('thresholdLevel', models.FloatField()),
            ],
        ),
    ]
