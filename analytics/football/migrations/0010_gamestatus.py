# Generated by Django 5.1 on 2024-08-17 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0009_alter_country_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='football.game')),
                ('status', models.CharField(choices=[('finished', 'FINISHED'), ('abandoned', 'ABANDONED'), ('forfeit', 'FORFEIT')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'game_statuses',
                'constraints': [models.UniqueConstraint(fields=('game', 'status'), name='unique_game_status')],
            },
        ),
    ]
