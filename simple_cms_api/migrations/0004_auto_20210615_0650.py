# Generated by Django 3.2.3 on 2021-06-15 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_cms_api', '0003_tenant_described_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenant',
            old_name='name',
            new_name='system_name',
        ),
        migrations.AddField(
            model_name='tenant',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
