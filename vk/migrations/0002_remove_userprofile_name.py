# Generated by Django 4.2 on 2023-05-02 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
    ]
