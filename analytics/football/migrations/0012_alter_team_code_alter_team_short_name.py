# Generated by Django 5.1 on 2024-10-04 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0011_fantasyfootballgameweek_gameweekgame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='short_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
