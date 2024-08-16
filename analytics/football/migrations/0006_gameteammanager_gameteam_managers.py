# Generated by Django 5.1 on 2024-08-14 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0005_competition_unique_competition_name_gender_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTeamManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.gameteam')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='football.manager')),
            ],
            options={
                'db_table': 'game_team_managers',
                'unique_together': {('game_team', 'manager')},
            },
        ),
        migrations.AddField(
            model_name='gameteam',
            name='managers',
            field=models.ManyToManyField(blank=True, related_name='game_teams', through='football.GameTeamManager', to='football.manager'),
        ),
    ]