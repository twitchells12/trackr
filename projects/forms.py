from django.contrib.admin import widgets
from django import forms
from .models import Project, Comment
from bootstrap_datepicker_plus import DatePickerInput

class ProjForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name','description','worker','completed_on','team','due_date']
        widgets = {
            'completed_on':DatePickerInput(),
            }

    def __init__(self, *args, **kwargs):
        self.fields['description'].widget.attrs['rows'] = 4
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["team"].queryset = (
                models.Team.objects.filter(
                    pk__in=user.teams.values_list("team__pk")
                )
            )
class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','title','text')