# PROJECTS URLS.py

from django.urls import path
from . import views

app_name='projects'

urlpatterns = [
    path('',views.ProjectList.as_view(),name='all'),
    path('new/',views.CreateProject.as_view(),name='create'),
    path('by/<username>/',views.UserProjects.as_view(),name='for_user'),
    path("project/<int:pk>/",views.ProjectDetail.as_view(),name="single"),
    path("delete/<int:pk>/",views.DeleteProject.as_view(),name="delete"),
    path("edit/<int:pk>/",views.EditProject.as_view(),name="edit"),
    path("worker/<pk>/",views.WorkerView.as_view(),name="worker"),
    path('project/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

]
