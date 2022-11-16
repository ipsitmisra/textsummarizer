from django.contrib import admin
from django.urls import path,include
from django.urls import path
from textsummarizer_app import views


urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("analyze", views.analyze, name="analyze"),
    path("analyze_url", views.analyze_url, name="analyze_url"),
]