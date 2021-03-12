from django.conf.urls import url
from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('login.html',lambda request: render(request,'login.html')),
    url(r'^$',views.dologin),
    url(r'^login/$',views.login),
    url(r'^forgotpassword/$',views.forgotpass),
    url(r'^testit/$',views.testit),
    url(r'^gotoresetlink/$',views.gotoresetlink),
    url(r'^resetpassword/$',views.resetpassword),
]