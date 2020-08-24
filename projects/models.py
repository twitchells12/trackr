from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from teams.models import Team
from datetime import date
from django import forms
# Create your models here.


status = (('Active','Active'),('Complete','Complete'),('On Hold','On Hold'))

class Project(models.Model):
    project_name = models.CharField(max_length=256)
    worker = models.ForeignKey(User,related_name='projects',null=True,on_delete=models.SET_NULL)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20,choices=status)
    completed_on = models.DateTimeField(blank=True,null=True)
    team = models.ForeignKey(Team,related_name='projects',null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.project_name

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('projects:all')

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    class Meta():
        ordering = ['-created_at']
        unique_together = ['worker','project_name']

class Comment(models.Model):
    project = models.ForeignKey(Project,null=True,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,related_name='author',null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    approved_comment = models.BooleanField(default=False,null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.title
