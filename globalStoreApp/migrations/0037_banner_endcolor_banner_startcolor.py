# Generated by Django 5.1.2 on 2024-10-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0036_banner_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='endColor',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='startColor',
            field=models.CharField(max_length=10, null=True),
        ),
    ]