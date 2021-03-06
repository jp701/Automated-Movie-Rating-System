from django.conf.urls import url
from registerapp import views

urlpatterns = [
    url(r'^$',views.doreg),
    url(r'^register/$',views.register),
]