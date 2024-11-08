# Generated by Django 4.2.7 on 2024-11-08 01:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SmartKitchen_App', '0019_recipeview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeview',
            old_name='rrecipe',
            new_name='recipe',
        ),
        migrations.AlterField(
            model_name='recipeview',
            name='viewed_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]