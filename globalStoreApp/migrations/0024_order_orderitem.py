# Generated by Django 5.1.1 on 2024-09-25 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0023_remove_order_product_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderItem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.orderitem'),
        ),
    ]
