# Generated by Django 5.1.1 on 2024-09-25 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0021_product_store_alter_featurelistmodel_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(blank=True, max_length=10)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ManyToManyField(to='globalStoreApp.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.store')),
            ],
        ),
    ]