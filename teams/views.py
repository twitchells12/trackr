from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect,render
from django.views import generic
from .models import Team,TeamMember
from .forms import TeamForm
from django.http import HttpResponseRedirect
from accounts.models import User

@login_required
def createTeam(request):
    form = TeamForm()

    if request.method == 'POST':
        form = TeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teams:all')
    context = {'form':form}
    return render(request,'teams/team_form.html',context)


class EditTeam(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = ('name','description','team_pic')
    template_name_suffix = '_update_form'
    def get_form(self):
        form = super().get_form()
        return form

class SingleTeam(LoginRequiredMixin,generic.DetailView):
    model = Team

class ListTeams(LoginRequiredMixin,generic.ListView):
    model = Team
    member = TeamMember

class ManageTeam(LoginRequiredMixin,generic.DetailView):
    model = Team
    member = TeamMember
    template_name_suffix = '_manage'

    def get_context_data(self, **kwargs):
        context = super(ManageTeam, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

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
            membership = TeamMember.objects.filter(
                user=self.request.user,
                team__slug=self.kwargs.get("slug")
            ).get()

        except TeamMember.DoesNotExist:
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


@login_required
def member_remove(request, pk):
    member = get_object_or_404(TeamMember, user__pk=pk)
    team_slug = Team.slug
    member.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def member_add(request, slug, pk):
    team = get_object_or_404(Team,slug=slug)
    worker = User.objects.get(pk=pk)
    TeamMember.objects.create(user=worker,team=team)
    # member.add()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
