# Generated by Django 5.0.6 on 2024-07-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organisations',
            field=models.ManyToManyField(related_name='users', to='organization.organization'),
        ),
    ]
