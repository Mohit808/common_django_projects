# Generated by Django 5.1.1 on 2024-09-10 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0007_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.variant'),
        ),
    ]