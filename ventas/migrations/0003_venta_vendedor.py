# Generated by Django 5.1 on 2024-11-20 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
        ('ventas', '0002_venta_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empleados.empleado'),
        ),
    ]
