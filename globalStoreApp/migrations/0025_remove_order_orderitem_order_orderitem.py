# Generated by Django 5.1.1 on 2024-09-25 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0024_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderItem',
        ),
        migrations.AddField(
            model_name='order',
            name='orderItem',
            field=models.ManyToManyField(null=True, to='globalStoreApp.orderitem'),
        ),
    ]
