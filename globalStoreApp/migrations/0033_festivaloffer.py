# Generated by Django 5.1.2 on 2024-10-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0032_rename_bannner_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='')),
                ('priority', models.SmallIntegerField()),
                ('category', models.ManyToManyField(to='globalStoreApp.variant')),
            ],
        ),
    ]
