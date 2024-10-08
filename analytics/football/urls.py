from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("league-tables/<str:competition_name>/<str:season_name>", views.league_table, name='league_table'),
    path("metrics-management/<str:competition_name>/<str:season_name>", views.metrics_management, name='metrics_management'),
    path('game/<int:game_id>/', views.game_view, name='game_view'),
] + debug_toolbar_urls()