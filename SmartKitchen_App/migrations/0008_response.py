# Generated by Django 4.2.7 on 2024-10-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartKitchen_App', '0007_mealplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('response', models.CharField(max_length=255)),
            ],
        ),
    ]
