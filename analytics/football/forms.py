from django import forms

from .enums import ExternalSource
from .models import GameTeamMetric, GameTeam


class GameTeamMetricForm(forms.ModelForm):
    game_team = forms.ModelChoiceField(queryset=GameTeam.objects.all(), widget=forms.HiddenInput())
    source = forms.CharField(widget=forms.HiddenInput(), initial=ExternalSource.FOT_MOB)

    class Meta:
        model = GameTeamMetric
        fields = ['game_team', 'source', 'xg', 'shots', 'shots_on_target']