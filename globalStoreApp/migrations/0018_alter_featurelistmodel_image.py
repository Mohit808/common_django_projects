# Generated by Django 5.1.1 on 2024-09-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0017_featurelistmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurelistmodel',
            name='image',
            field=models.ImageField(blank=True, upload_to='product_images'),
        ),
    ]