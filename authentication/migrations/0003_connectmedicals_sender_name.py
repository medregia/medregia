# Generated by Django 5.0.6 on 2024-07-11 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_registermedicals_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectmedicals',
            name='sender_name',
            field=models.CharField(editable=False, max_length=30, null=True),
        ),
    ]
