from django.conf.urls import url
from django.shortcuts import render
from django.urls import path
from userapp import views

urlpatterns = [
    url(r'^$',views.readExcel),
    url(r'^user_home/$',views.user_home),
    url(r'^calculateRating/$',views.calculateRating),
    url(r'^addReview/$',views.addReview),
    url(r'^showmovie/$',views.showmovie),
    url(r'^reviews/$',views.my_reviews),
    url(r'^update_review/$',views.update_review),
    url(r'^delete_review/$',views.delete_review),
    url(r'^profile/$',views.profile),
    url(r'^update_profile/$',views.update_profile),
    path('settings.html',lambda request: render(request,'settings.html')),
]