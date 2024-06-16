# Generated by Django 4.2.3 on 2024-06-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_registermedicals_uniqueid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='DrugLiceneseNumber1',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='DrugLiceneseNumber2',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='MedicalShopName',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='ProprietaryContact',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='ProprietaryName',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='ProprietaryNumber',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='RegisteredNumber',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
