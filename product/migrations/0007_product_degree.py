# Generated by Django 5.0.3 on 2024-04-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='degree',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
