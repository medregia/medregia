# Generated by Django 4.2.9 on 2024-02-08 08:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invclc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
