# Generated by Django 5.1 on 2024-08-14 11:43

from django.db import migrations

def populate_data(apps, schema_editor):
    Confederation = apps.get_model('football', 'Confederation')

    Confederation.objects.create(code='AFC', name='Asian Football Confederation')
    Confederation.objects.create(code='CAF', name='Confederation of African Football')
    Confederation.objects.create(code='CONCACAF', name='Confederation of North, Central American and Caribbean Association Football')
    Confederation.objects.create(code='CONMEBOL', name='South American Football Confederation')
    Confederation.objects.create(code='OFC', name='Oceania Football Confederation')
    Confederation.objects.create(code='UEFA', name='Union of European Football Associations')

def delete_data(apps, schema_editor):
    Confederation = apps.get_model('football', 'Confederation')

    Confederation.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('football', '0006_gameteammanager_gameteam_managers'),
    ]

    operations = [
        migrations.RunPython(populate_data, reverse_code=delete_data),
    ]
