# Generated by Django 5.0.6 on 2024-07-07 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_user_options_remove_user_date_joined_and_more'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Organization',
            new_name='Organisation',
        ),
    ]
