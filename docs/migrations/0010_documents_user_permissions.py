# Generated by Django 5.1 on 2024-09-14 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0009_documents_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='user_permissions',
            field=models.JSONField(default=dict),
        ),
    ]