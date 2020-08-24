from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.ListTeams.as_view(), name="all"),
    path("new/", views.CreateTeam.as_view(), name="create"),
    path("manage/<slug>", views.ManageTeam.as_view(), name="manage"),
    path("delete/<slug>", views.DeleteTeam.as_view(), name="delete"),
    path("teams/in/<slug>/",views.SingleTeam.as_view(),name="single"),
    path("join/<slug>/",views.JoinTeam.as_view(),name="join"),
    path("leave/<slug>/",views.LeaveTeam.as_view(),name="leave"),
    path('teams/in/<slug>/members',views.MemberList.as_view(),name='members'),

]
