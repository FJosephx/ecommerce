# Generated by Django 5.2 on 2025-05-07 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_pedido_email_pedido_nombre_receptor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='telefono',
            field=models.CharField(default='', help_text='Número de WhatsApp/contacto', max_length=20),
        ),
    ]
