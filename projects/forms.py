from django.contrib.admin import widgets
from django import forms
from .models import Project, Comment, Attachment
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth import get_user_model
User=get_user_model()

class ProjForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name','description','created_by','workers',
                    'completed_on','team','due_date']
        widgets = {
            'completed_on':DatePickerInput(),
            'workers': forms.CheckboxSelectMultiple(),
            }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if user is not None:
    #         self.fields["team"].queryset = (
    #             models.Team.objects.filter(
    #                 pk__in=user.teams.values_list("team__pk")
    #             )
    #         )
    def __init__(self,*args,**kwargs):
        super(ProjForm, self).__init__(*args, **kwargs)
        self.fields["workers"].widget = forms.CheckboxSelectMultiple()



class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

class AttachForm(forms.ModelForm):

    class Meta():
        model = Attachment
        fields = ('file','added_by')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.widget.attrs.update({'size': '12'})
