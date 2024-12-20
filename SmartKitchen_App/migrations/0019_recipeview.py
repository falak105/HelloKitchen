# Generated by Django 4.2.7 on 2024-11-08 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SmartKitchen_App', '0018_alter_healthanalysis_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('rrecipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SmartKitchen_App.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
