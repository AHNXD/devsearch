from django.urls import path
from . import views

urlpatterns = [
    #path('projects/', views.projects, name='Projects'),
    path('', views.projects, name='Projects'),
    path('project/<str:id>/', views.project, name='Project'),
    path('create-project/', views.createProject, name='CreateProject'),
    path('update-project/<str:id>/', views.updateProject, name='UpdateProject'),
    path('delete-project/<str:id>/', views.deleteProject, name='DeleteProject'),
    path('remove-tag/<str:p_id>&<str:t_id>/', views.removeTag, name='RemoveTag'),
]

