# Generated by Django 5.1.1 on 2024-09-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0014_alter_category_main_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='highlight',
            field=models.TextField(blank=True),
        ),
    ]