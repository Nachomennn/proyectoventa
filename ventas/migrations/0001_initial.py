# Generated by Django 5.1 on 2024-11-20 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total_neto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_con_iva', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_documento', models.CharField(max_length=20)),
                ('metodo_pago', models.CharField(max_length=20)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='VentaDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.venta')),
            ],
        ),
        migrations.AddField(
            model_name='venta',
            name='productos',
            field=models.ManyToManyField(through='ventas.VentaDetalle', to='productos.producto'),
        ),
    ]
