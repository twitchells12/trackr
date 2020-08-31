from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404,request
from django.views import generic
from bootstrap_datepicker_plus import DatePickerInput
from .forms import ProjForm, CommentForm, AttachForm
from .models import Project,Comment, Attachment
from accounts.models import UserProfile
from django.contrib.auth.models import User
from teams.models import Team,TeamMember
from .filters import ProjectFilter

@login_required
def projectList(request):
    projects = Project.objects.all()

    myFilter = ProjectFilter(request.GET, queryset=projects)
    projects = myFilter.qs

    for project in projects:
        project.checkStatus()
    context = {'projects':projects,'myFilter':myFilter}
    return render(request, 'projects/project_list.html',context)

@login_required
def userProjects(request):
    projects = Project.objects.filter(worker=request.user)
    project_user = User.objects.prefetch_related("projects").get(
                                    username__iexact=request.user.username)

    context = {'projects':projects,'project_user':project_user}
    return render(request, 'projects/user_project_list.html',context)


class ProjectDetail(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['files'] = Attachment.objects.all()
        return context

class CreateProject(LoginRequiredMixin, generic.CreateView):
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

class EditProject(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = ['description','status','worker','due_date','completed_on','team']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy("projects:all")
    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = DatePickerInput()
        form.fields['completed_on'].widget = DatePickerInput()
        return form

class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("projects:all")

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Project Deleted")
        return super().delete(*args, **kwargs)

class WorkerView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'projects/worker_profile.html'

@login_required
def completeProject(request, pk):
    projects = Project.objects.get(pk=pk)
    projects.markComplete()
    return redirect ('projects:single', pk=projects.pk)


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
        form.fields['author'].initial = request.user
    return render(request, 'projects/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.project.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    project_pk = comment.project.pk
    comment.delete()
    return redirect('projects:single', pk=project_pk)



@login_required
def add_file(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = AttachForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.project = project
            file.save()
            return redirect('projects:single', pk=project.pk)
    else:
        form = AttachForm()
        form.fields['added_by'].initial = request.user
    return render(request, 'projects/attachment_form.html', {'form': form})
