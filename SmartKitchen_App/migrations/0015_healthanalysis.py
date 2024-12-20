# Generated by Django 4.2.7 on 2024-11-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartKitchen_App', '0014_delete_healthanalysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('level', models.DecimalField(decimal_places=2, max_digits=5)),
                ('health_issue', models.CharField(choices=[('Diabetes', 'Diabetes'), ('Hypertension', 'Hypertension'), ('Obesity', 'Obesity'), ('High Cholesterol', 'High Cholesterol'), ('Sugar', 'High Sugar'), ('Other', 'Other')], max_length=50)),
                ('other_health_issue', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
