# Generated by Django 5.1.1 on 2024-09-30 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0025_remove_order_orderitem_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('mobile', models.ImageField(blank=True, max_length=20, upload_to='')),
                ('email', models.ImageField(blank=True, max_length=50, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(max_length=10)),
                ('address_title', models.CharField(max_length=200)),
                ('full_address', models.CharField(max_length=200)),
                ('house_no', models.CharField(blank=True, max_length=100)),
                ('area', models.CharField(blank=True, max_length=100)),
                ('landmark', models.CharField(blank=True, max_length=100)),
                ('instruction', models.CharField(blank=True, max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.customer')),
            ],
        ),
    ]
