# Generated by Django 4.2.3 on 2024-03-23 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_userloginactivity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserLoginActivity',
        ),
    ]
