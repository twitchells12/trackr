import os
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from teams.models import Team
from datetime import date
from django import forms
# Create your models here.


status = (('Active','Active'),('Complete','Complete'),('On Hold','On Hold'),('Past Due','Past Due'))


def get_attachment_upload_dir(instance, filename):
    return "/".join(["projects", "attachments", str(instance.project.id), filename])

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=256)
    workers = models.ManyToManyField(User,through='ProjectWorker')
    created_by = models.ForeignKey(User,related_name='created',null=True,on_delete=models.SET_NULL)
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

    def checkStatus(self):
        today = date.today()
        dt = self.due_date.date()
        if dt < today:
            self.status = 'Past Due'
        self.save()

    def markComplete(self):
        today = date.today()
        self.completed_on = today
        self.status = 'Complete'
        self.save()

    class Meta():
        ordering = ['-created_at']

class ProjectWorker(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='assigned_to')
    assignee = models.ForeignKey(User,related_name='proj_worker',on_delete=models.CASCADE)


class Comment(models.Model):
    project = models.ForeignKey(Project,null=True,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,related_name='author',null=True,on_delete=models.CASCADE)
    text = models.CharField(max_length=256,blank=True,null=True)
    approved_comment = models.BooleanField(default=False,null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.title

class Attachment(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='attachments')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_attachment_upload_dir, max_length=255)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"{self.project.id} - {self.file.name}"

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='task')
    task = models.CharField(max_length=256,null=True,blank=True)
    completed = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return self.task
