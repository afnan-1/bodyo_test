# Generated by Django 3.2 on 2022-05-21 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='bithdate',
            new_name='birthdate',
        ),
    ]
