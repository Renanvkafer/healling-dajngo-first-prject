# Generated by Django 5.0.4 on 2024-04-18 17:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0004_alter_datasabertas_agendado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DatasAbertas',
            new_name='DatasAbertt',
        ),
    ]
