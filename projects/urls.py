# PROJECTS URLS.py
from django.urls import path
from . import views

app_name='projects'

urlpatterns = [
    path('',views.projectList,name='all'),
    path('new/',views.CreateProject.as_view(),name='create'),
    path('by/',views.userProjects,name='for_user'),
    path("project/<int:pk>/attach",views.add_file,name="add_file"),
    path("project/<int:pk>/",views.projectDetail,name="detail"),

    path("delete/<int:pk>/",views.DeleteProject.as_view(),name="delete"),
    path("complete/<int:pk>/",views.completeProject,name="complete"),
    path("edit/<int:pk>/",views.EditProject.as_view(),name="edit"),
    path("worker/<pk>/",views.WorkerView.as_view(),name="worker"),
    path('project/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

]
