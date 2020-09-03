from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Project
from datetime import date

@login_required
def homePage(request):
    projects = Project.objects.all()
    for project in projects:
        project.checkStatus()

    context = {
        'active': Project.objects.filter(status='Active').count(),
        'hold' : Project.objects.filter(status='On Hold').count(),
        'complete' : Project.objects.filter(status='Complete').count(),
        'past_due' : Project.objects.filter(status='Past Due').count(),
    }
    return render(request, 'index.html',context)
