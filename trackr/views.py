from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.contrib import messages
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



class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = Project.objects.filter(status='Active').count()
        context['hold'] = Project.objects.filter(status='On Hold').count()
        context['complete'] = Project.objects.filter(status='Complete').count()
        context['past_due'] = Project.objects.filter(status='Past Due').count()
        return context
