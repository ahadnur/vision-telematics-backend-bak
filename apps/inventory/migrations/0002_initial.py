# Generated by Django 5.0.6 on 2025-05-04 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='product_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='products.productsku'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_movements', to='inventory.inventory'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='product_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_movements', to='products.productsku'),
        ),
    ]
