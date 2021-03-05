from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^user_home/',views.user_home),
    url(r'^add_review/',views.add_review),
]