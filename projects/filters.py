import django_filters
from django_filters import DateFilter, CharFilter,NumberFilter
from .models import Project
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class ProjectFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name='completed_on',lookup_expr='gte')
    # end_date = DateFilter(field_name='completed_on',lookup_expr='lte')
    project_name = CharFilter(field_name='project_name',lookup_expr='icontains')
    id = NumberFilter(field_name='id')
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['description','completed_on','created_at','created_by']

        widgets = {
            'id': forms.TextInput(attrs={'class':"form-control"}),
            'project_name': forms.TextInput(attrs={'class':"form-control"}),
            'due_date':DatePickerInput(attrs={'class':"form-control"}),
            'worker':forms.Select(attrs={'class':"form-control"}),
            'status': forms.Select(attrs={'class':"form-control"}),
            'team': forms.Select(attrs={'class':"form-control"}),
        }
