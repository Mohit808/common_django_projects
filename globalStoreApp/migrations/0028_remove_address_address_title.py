# Generated by Django 5.1.1 on 2024-09-30 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0027_alter_customer_email_alter_customer_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_title',
        ),
    ]