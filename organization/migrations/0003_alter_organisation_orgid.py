# Generated by Django 5.0.6 on 2024-07-07 22:15

import organization.generate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_rename_organization_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='orgId',
            field=models.CharField(default=organization.generate.generate_org_id, max_length=255, unique=True),
        ),
    ]
