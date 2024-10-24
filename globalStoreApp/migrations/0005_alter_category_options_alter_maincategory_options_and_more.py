# Generated by Django 5.1.1 on 2024-09-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalStoreApp', '0004_maincategory_category_main_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='maincategory',
            options={'verbose_name': 'MainCategory', 'verbose_name_plural': 'MainCategories'},
        ),
        migrations.AlterField(
            model_name='maincategory',
            name='image',
            field=models.ImageField(blank=True, upload_to='product_images'),
        ),
    ]
