# Generated by Django 5.1 on 2024-10-11 07:57

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0014_gameexternallink'),
    ]

    operations = [
        migrations.CreateModel(
            name='StageTeamMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='team_metrics', to='football.stage')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage_metrics', to='football.team')),
                ('source', models.CharField(choices=[('football-data.co.uk', 'FOOTBALL_DATA'), ('Understat', 'UNDERSTAT'), ('FotMob', 'FOT_MOB')], max_length=200)),
                ('xg', models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('xg_against', models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('x_points', models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(999.99)])),
                ('points', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'stage_team_metrics',
                'constraints': [models.UniqueConstraint(fields=('stage', 'team', 'source'), name='unique_stage_team_source')],
            },
        ),
    ]
