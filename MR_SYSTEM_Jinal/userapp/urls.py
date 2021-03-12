from django.conf.urls import url
from userapp import views

urlpatterns = [
    url(r'^reviews/$',views.my_reviews),
    url(r'^update_review/$',views.update_review),
    url(r'^delete_review/$',views.delete_review),
    url(r'^profile/$',views.profile),
    url(r'^update_profile/$',views.update_profile),
]