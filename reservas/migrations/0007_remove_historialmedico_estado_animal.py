# Generated by Django 5.1 on 2024-09-16 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0006_remove_historialmedico_resultado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialmedico',
            name='estado_animal',
        ),
    ]
