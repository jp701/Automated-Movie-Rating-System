from django.conf.urls import url
from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns=[
    url(r'^user_home_initial/',views.readExcel),
    url(r'^user_home/',views.user_home),
    url(r'^calculateRating/',views.calculateRating),
    url(r'^addReview/',views.addReview),
    url(r'^showmovie/',views.showmovie),
    url(r'^clogout/',views.clogout),
    path('settings.html',lambda request: render(request,'settings.html')),
]