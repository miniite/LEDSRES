# Generated by Django 5.0.2 on 2024-05-05 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile_priivate_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='priivate_address',
            new_name='private_address',
        ),
        migrations.AddField(
            model_name='auction',
            name='contract_id',
            field=models.IntegerField(default=0),
        ),
    ]
