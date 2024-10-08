# Generated by Django 5.1 on 2024-08-17 10:29

import django.db.models.deletion
from django.db import migrations, models

from football.enums import GameweekType


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0010_gamestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyFootballGameweek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(choices=[('fpl', 'FPL'), ('efl', 'EFL'), ('fantrax', 'FANTRAX')], max_length=50)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fantasy_football_gameweeks', to='football.stage')),
                ('number', models.IntegerField()),
                ('gameweek_type', models.CharField(choices=[('single', 'SINGLE'), ('double', 'DOUBLE'), ('triple', 'TRIPLE')], default=GameweekType['SINGLE'], max_length=20)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fantasy_football_gameweeks',
                'constraints': [models.UniqueConstraint(fields=('provider', 'stage', 'number'), name='unique_provider_stage_number')],
            },
        ),
        migrations.CreateModel(
            name='GameweekGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='gameweek_games', to='football.game')),
                ('gameweek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek_games', to='football.fantasyfootballgameweek')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fantasy_football_gameweek_games',
                'constraints': [models.UniqueConstraint(fields=('gameweek', 'game'), name='unique_gameweek_game')],
            },
        ),
    ]
