# Generated by Django 5.1.1 on 2024-09-13 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0016_remove_product_tag_product_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('highlight', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='product_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.category')),
                ('main_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.maincategory')),
                ('tag', models.ManyToManyField(blank=True, null=True, to='globalStoreApp.tags')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.variant')),
            ],
        ),
    ]