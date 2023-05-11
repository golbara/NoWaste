# Generated by Django 4.1.7 on 2023-05-11 22:57

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VC_Codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('vc_code', models.CharField(max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MyAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(4)])),
                ('role', models.CharField(default='customer', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('myauthor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('restaurant_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=2)),
                ('number', models.CharField(blank=True, max_length=11, null=True)),
                ('purches_counts', models.IntegerField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, default=0.0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('count_rates', models.IntegerField(blank=True, default=0, null=True)),
                ('date_of_establishment', models.DateField(default=datetime.date(2023, 5, 12))),
                ('description', models.CharField(default='', max_length=1024)),
            ],
            options={
                'abstract': False,
            },
            bases=('User.myauthor',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('myauthor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.CharField(default='', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(default=models.CharField(max_length=255), max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(regex='^\\d{10}$')])),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('wallet_balance', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True)),
                ('list_of_favorites_res', models.ManyToManyField(blank=True, null=True, related_name='cust_favor_list', to='User.restaurant')),
            ],
            options={
                'abstract': False,
            },
            bases=('User.myauthor',),
        ),
    ]
