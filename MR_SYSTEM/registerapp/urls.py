from django.conf.urls import url
from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$',views.index),
    path('register.html',lambda request: render(request,'register.html')),
    url(r'^register/$',views.register),
]