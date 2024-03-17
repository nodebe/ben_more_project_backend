from django.contrib import admin
from django.urls import path

from project.views import ProjectApiView, ProjectOptionsApiView


urlpatterns = [
    path('', ProjectApiView.as_view()),
    path('<str:pid>', ProjectApiView.as_view()),
    path('options', ProjectOptionsApiView.as_view())
]