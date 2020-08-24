from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.contrib import messages

class HomePage(TemplateView):
    template_name = 'index.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = Project.objects.filter(status='Active').count()
        context['hold'] = Project.objects.filter(status='On Hold').count()
        context['complete'] = Project.objects.filter(status='Complete').count()
        return context
