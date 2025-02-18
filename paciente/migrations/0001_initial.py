# Generated by Django 5.0.4 on 2024-04-20 08:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medico', '0013_alter_medico_datas_agendado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('link', models.URLField(blank=True, null=True)),
                ('data_aberta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medico.medico_datas')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
