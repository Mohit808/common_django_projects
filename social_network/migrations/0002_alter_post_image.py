# Generated by Django 5.1.6 on 2025-03-18 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.TextField(null=True),
        ),
    ]
