from django.conf.urls import url
from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$',views.admin_home),
    url(r'^add_movie/$',views.addmovie),
    url(r'^showmovies/$',views.showmovies),
    url(r'^showmovie/$',views.showmovie),
    url(r'^updatemovie/$',views.updatemovie),
    url(r'^deletemovie/$',views.deletemovie),
    path('addmovie.html',lambda request: render(request,'addmovie.html')),
    path('settings.html',lambda request: render(request,'settings.html')),
    path('showmovie.html',lambda request: render(request,'showmovie.html'))
]