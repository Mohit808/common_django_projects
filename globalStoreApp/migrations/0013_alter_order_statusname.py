# Generated by Django 5.0 on 2024-12-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("globalStoreApp", "0012_alter_store_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="statusName",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
