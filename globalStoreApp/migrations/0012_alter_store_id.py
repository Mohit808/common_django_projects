# Generated by Django 5.0 on 2024-12-14 15:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("globalStoreApp", "0011_alter_store_store_banner_alter_store_store_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
