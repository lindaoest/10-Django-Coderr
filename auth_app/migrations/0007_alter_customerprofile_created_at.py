# Generated by Django 5.2.1 on 2025-05-20 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0006_alter_customerprofile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
