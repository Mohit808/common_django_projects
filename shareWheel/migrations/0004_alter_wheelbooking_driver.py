# Generated by Django 5.1.2 on 2024-10-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareWheel', '0003_alter_wheelbooking_driver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wheelbooking',
            name='driver',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
