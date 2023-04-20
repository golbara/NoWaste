# Generated by Django 4.1.7 on 2023-04-20 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('ingredients', models.CharField(blank=True, max_length=2048, null=True)),
                ('food_pic', models.ImageField(blank=True, null=True, upload_to='Food_pics/')),
                ('Type', models.CharField(blank=True, choices=[('drink', 'Drink'), ('iranian_food', 'Iranian_food'), ('foreign_food', 'Foreign_food')], max_length=255)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='User.restaurant')),
            ],
        ),
    ]
