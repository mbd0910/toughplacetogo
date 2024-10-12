from django.contrib import admin

from football.models import Competition, CompetitionExternalLink, Confederation, Country, Game, GameTeam, Stage, StagePointsDeduction, Team, TeamExternalLink

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'competition_type', 'country', 'confederation')

class CompetitionExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('competition', 'source', 'external_link_type', 'value')

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

class StageAdmin(admin.ModelAdmin):
    list_display = ('season', 'name')
    ordering = ['season', 'name']

class StagePointsDeductionAdmin(admin.ModelAdmin):
    list_display = ('stage__season', 'stage', 'team', 'deduction')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'code', 'gender', 'team_type', 'country', 'confederation')
    ordering = ['name']

class TeamExternalLinkAdmin(admin.ModelAdmin):
    list_display = ('team', 'source', 'external_link_type', 'value')
    ordering = ['team', 'source', 'external_link_type', 'value']

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionExternalLink, CompetitionExternalLinkAdmin)
admin.site.register(Confederation, ConfederationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameTeam, GameTeamAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(StagePointsDeduction, StagePointsDeductionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamExternalLink, TeamExternalLinkAdmin)