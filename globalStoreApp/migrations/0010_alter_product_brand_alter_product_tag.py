# Generated by Django 5.1.1 on 2024-09-10 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0009_product_main_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.tags'),
        ),
    ]