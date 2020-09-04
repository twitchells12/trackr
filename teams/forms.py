from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from .models import Team, TeamMember


class TeamForm(ModelForm):

    class Meta():
        model = Team
        fields = ("name", "description",'team_pic')
