from django.contrib import admin

from football.models import Confederation, Country, Game, GameTeam, Team, TeamExternalLink

class ConfederationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    ordering = ['code']

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'confederation')
    ordering = ['name']

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'kickoff', 'stage', 'finished', 'venue')
    ordering = ['kickoff']

class GameTeamAdmin(admin.ModelAdmin):
    list_display = ('number', 'game', 'game__name', 'team', 'half_time_score', 'full_time_score', 'after_extra_time_score')
    ordering = ['id', 'number']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'code', 'gender', 'team_type', 'country', 'confederation')
    ordering = ['name']

class TeamExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('team', 'source', 'external_link_type', 'value')
    ordering = ['team', 'source', 'external_link_type', 'value']

admin.site.register(Confederation, ConfederationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameTeam, GameTeamAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamExternalLink, TeamExternalLinkAdmin)