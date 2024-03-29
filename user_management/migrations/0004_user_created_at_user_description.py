# Generated by Django 5.0.3 on 2024-03-22 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
