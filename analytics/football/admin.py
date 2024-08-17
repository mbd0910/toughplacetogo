from django.contrib import admin

from football.models import Confederation, Country, Team, TeamExternalLink

class ConfederationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    ordering = ['code']

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'confederation')
    ordering = ['name']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'code', 'gender', 'team_type', 'country', 'confederation')
    ordering = ['name']

class TeamExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('team', 'source', 'external_link_type', 'value')
    ordering = ['team', 'source', 'external_link_type', 'value']

admin.site.register(Confederation, ConfederationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamExternalLink, TeamExternalLinkAdmin)