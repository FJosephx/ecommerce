# Generated by Django 5.2 on 2025-05-07 03:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0004_pedido_telefono'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tienda.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tienda.producto')),
            ],
        ),
    ]
