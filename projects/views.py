from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import Http404,request
from django.views import generic
from bootstrap_datepicker_plus import DatePickerInput
from .forms import ProjForm, CommentForm, AttachForm
from accounts.forms import UserProfileForm
from .models import Project,Comment, Attachment,Task
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
    projects = Project.objects.filter(workers=request.user)
    project_user = User.objects.prefetch_related("proj_worker").get(
                                    username__iexact=request.user.username)

    context = {'projects':projects,'project_user':project_user}
    return render(request, 'projects/user_project_list.html',context)



def handle_add_comment(request, project):
    if not request.POST.get("add_comment"):
        return
    Comment.objects.create(author=request.user, project=project, text=request.POST["comment-body"])



@login_required
def projectDetail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comments = Comment.objects.all()
    attachments = Attachment.objects.all()
    handle_add_comment(request, project)

    if request.FILES.get("attachment_file_input"):
        file = request.FILES.get("attachment_file_input")

        Attachment.objects.create(
            project=project, added_by=request.user, file=file
        )
        return redirect("projects:detail", pk=project.pk)

    context = {'project':project,'comments':comments,'attachments':attachments}

    return render(request, 'projects/project_detail.html',context)



class CreateProject(LoginRequiredMixin, generic.CreateView):
    fields = ['project_name','description','created_by','workers','status','due_date','completed_on','team']
    model = Project

    def get_form(self):
        form = super().get_form()
        form.fields['due_date'].widget = DatePickerInput()
        form.fields['completed_on'].widget = DatePickerInput()
        form.fields['workers'].initial = self.request.user
        form.fields['created_by'].initial = self.request.user
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

class EditProject(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = ['description','status','workers','due_date','completed_on','team']
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



@login_required
def workerView(request,pk):
    worker = UserProfile.objects.get(pk=pk)
    # profile = UserProfileForm(instance=worker)
    teamlist = list(Team.objects.filter(members=request.user))
    context = {'worker':worker,'teamlist':teamlist}
    return render(request, 'projects/worker_profile.html',context)



class WorkerView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'projects/worker_profile.html'

@login_required
def completeProject(request, pk):
    projects = Project.objects.get(pk=pk)
    projects.markComplete()
    return redirect ('projects:detail', pk=projects.pk)


@login_required
def add_comment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.save()
            return redirect('projects:detail', pk=project.pk)
    else:
        form = CommentForm()
        form.fields['author'].initial = request.user
    return render(request, 'projects/comment_form.html', {'form': form,'project':project})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('project_detail', pk=comment.project.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    project_pk = comment.project.pk
    comment.delete()
    return redirect('projects:detail', pk=project_pk)



@login_required
def add_file(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = AttachForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.project = project
            file.save()
            return redirect('projects:detail', pk=project.pk)
    else:
        form = AttachForm()
        form.fields['added_by'].initial = request.user
    return render(request, 'projects/attachment_form.html', {'form': form})
