# Generated by Django 5.0.3 on 2024-03-22 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_product_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(default='Chưa duyệt', max_length=100),
        ),
    ]
