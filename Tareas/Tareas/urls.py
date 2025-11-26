"""
URL configuration for Tareas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from TareasApp import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),

    path('profile/', views.profile_view, name='profile_view'),
    path('users/', views.user_list, name='user_list'),
    path('tasks/personal', views.my_tasks, name='my_tasks'),
    path('tasks/validate', views.tasks_to_validate, name='tasks_to_validate'),

    path('tasks/create/individual', views.create_individual_task, name='create_individual_task'),
    path('tasks/create/group', views.create_group_task, name='create_group_task')
]
