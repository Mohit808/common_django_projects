# Generated by Django 5.0 on 2024-12-12 20:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("globalStoreApp", "0010_alter_store_gst_number_alter_store_pan_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="store_banner",
            field=models.ImageField(upload_to=""),
        ),
        migrations.AlterField(
            model_name="store",
            name="store_logo",
            field=models.ImageField(upload_to=""),
        ),
    ]
