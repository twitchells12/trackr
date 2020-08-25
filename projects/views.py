from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404,request
from django.views import generic
from bootstrap_datepicker_plus import DatePickerInput
from braces.views import SelectRelatedMixin
from django.db.models import Count
from .forms import ProjForm, CommentForm
from .models import Project,Comment
from accounts.models import UserProfile
from django.contrib.auth.models import User
from teams.models import Team,TeamMember
from datetime import date
from datetime import datetime

@login_required
def projectList(request):
    projects = Project.objects.all()
    today = date.today()
    for project in projects:
        dt = project.due_date.date()
        if dt < today:
            project.status = 'Past Due'
    context = {'projects':projects}
    return render(request, 'projects/project_list.html',context)


@login_required
def userProjects(request):
    projects = Project.objects.filter(worker=request.user)
    project_user = User.objects.prefetch_related("projects").get(
                                    username__iexact=request.user.username)
    today = date.today()
    for project in projects:
        dt = project.due_date.date()
        if dt < today:
            project.status = 'Past Due'

    context = {'projects':projects,'project_user':project_user}
    return render(request, 'projects/user_project_list.html',context)


class ProjectDetail(SelectRelatedMixin, LoginRequiredMixin,generic.DetailView):
    model = Project
    comments = Comment
    select_related = ("worker",)


class CreateProject(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ['project_name','description','created_by','worker','status','due_date','completed_on','team']
    model = Project

    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = DatePickerInput()
        form.fields['completed_on'].widget = DatePickerInput()
        form.fields['worker'].initial = self.request.user
        form.fields['created_by'].initial = self.request.user
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.worker = self.request.user
        self.object.save()
        return super().form_valid(form)

class EditProject(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    model = Project
    select_related = ("worker",)
    fields = ['description','status','worker','due_date','completed_on','team']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("projects:all")
    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = DatePickerInput()
        form.fields['completed_on'].widget = DatePickerInput()
        return form

class DeleteProject(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Project
    select_related = ("worker",)
    success_url = reverse_lazy("projects:all")

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Project Deleted")
        return super().delete(*args, **kwargs)

class WorkerView(LoginRequiredMixin,SelectRelatedMixin,generic.DetailView):
    model = Project
    select_related = ("worker",)
    template_name = 'projects/worker_profile.html'



@login_required
def add_comment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.save()
            return redirect('projects:single', pk=project.pk)
    else:
        form = CommentForm()
    return render(request, 'projects/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.project.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.project.pk)
