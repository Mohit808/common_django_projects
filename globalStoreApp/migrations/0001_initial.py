# Generated by Django 5.1.1 on 2024-09-10 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product_images')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product_images')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OtpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('otp', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('whatsapp_number', models.CharField(max_length=20)),
                ('profile_image', models.CharField(max_length=100)),
                ('role_id', models.CharField(max_length=10)),
                ('social_login_type', models.CharField(max_length=10)),
                ('social_login_id', models.CharField(max_length=100)),
                ('is_phone_number_verified', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('aadhaar_number', models.CharField(max_length=12)),
                ('is_aadhar_verified', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('fcm_token', models.CharField(max_length=100)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product_images')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100)),
                ('store_slug', models.CharField(max_length=100)),
                ('business_name', models.CharField(max_length=100)),
                ('store_logo', models.CharField(max_length=100)),
                ('store_banner', models.CharField(max_length=100)),
                ('store_story', models.CharField(max_length=100)),
                ('store_type', models.CharField(max_length=100)),
                ('gst_number', models.CharField(max_length=12)),
                ('pan_number', models.CharField(max_length=10)),
                ('store_description', models.CharField(max_length=100)),
                ('service_type', models.CharField(max_length=10)),
                ('categories', models.CharField(max_length=100)),
                ('store_code', models.CharField(max_length=100)),
                ('store_code_text', models.CharField(max_length=100)),
                ('loyalty_points', models.CharField(max_length=10)),
                ('store_address', models.CharField(max_length=100)),
                ('store_building', models.CharField(blank=True, max_length=100)),
                ('store_floor', models.CharField(blank=True, max_length=100)),
                ('store_tower', models.CharField(blank=True, max_length=100)),
                ('store_landmark', models.CharField(blank=True, max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('store_how_to_reach', models.CharField(blank=True, max_length=100)),
                ('store_country', models.CharField(max_length=100)),
                ('store_state', models.CharField(max_length=100)),
                ('store_city', models.CharField(max_length=100)),
                ('lat', models.CharField(max_length=10)),
                ('lng', models.CharField(max_length=10)),
                ('subscription_plan_id', models.CharField(max_length=10)),
                ('store_visibility', models.CharField(max_length=10)),
                ('store_status', models.CharField(max_length=10)),
                ('store_privacy_policy', models.CharField(max_length=100)),
                ('store_tnc', models.CharField(max_length=100)),
                ('store_refund_policy', models.CharField(max_length=100)),
                ('is_pickup', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='product_images')),
                ('price', models.FloatField()),
                ('discountedPrice', models.FloatField()),
                ('origin', models.TextField()),
                ('tips', models.TextField()),
                ('additional_info', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.category')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='globalStoreApp.tags')),
            ],
        ),
    ]
