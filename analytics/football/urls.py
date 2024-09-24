from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("league-tables/<str:competition_name>/<str:season_name>", views.league_table)
]