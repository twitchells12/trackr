from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from teams.models import Team,TeamMember
from . import models


class CreateTeam(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description",'team_pic')
    model = Team

class SingleTeam(LoginRequiredMixin,generic.DetailView):
    model = Team

class ListTeams(LoginRequiredMixin,generic.ListView):
    model = Team
    member = TeamMember

class ManageTeam(LoginRequiredMixin,generic.DetailView):
    model = Team
    member = TeamMember
    fields = ("name", "description")
    template_name_suffix = '_manage'


class DeleteTeam(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("teams:all")

class JoinTeam(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("teams:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team,slug=self.kwargs.get("slug"))

        try:
            TeamMember.objects.create(user=self.request.user,team=team)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(team.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(team.name))

        return super().get(request, *args, **kwargs)


class LeaveTeam(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("teams:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.TeamMember.objects.filter(
                user=self.request.user,
                team__slug=self.kwargs.get("slug")
            ).get()

        except models.TeamMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)

class MemberList(LoginRequiredMixin,generic.DetailView):
    model = Team
    template_name_suffix = '_members'
