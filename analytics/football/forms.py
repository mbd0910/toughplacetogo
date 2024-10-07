from django import forms

from .enums import ExternalSource
from .models import GameTeamMetric


class GameTeamMetricForm(forms.ModelForm):
    game_team_id = forms.IntegerField(widget=forms.HiddenInput())
    source = forms.CharField(widget=forms.HiddenInput(), initial=ExternalSource.FOT_MOB)

    class Meta:
        model = GameTeamMetric
        fields = ['game_team_id', 'source', 'xg', 'shots', 'shots_on_target']