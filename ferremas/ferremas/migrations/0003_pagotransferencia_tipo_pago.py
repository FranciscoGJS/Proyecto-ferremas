# Generated by Django 5.1.1 on 2025-06-01 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferremas', '0002_remove_pagotransferencia_comprobante'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagotransferencia',
            name='tipo_pago',
            field=models.CharField(default='transferencia', max_length=20),
        ),
    ]
