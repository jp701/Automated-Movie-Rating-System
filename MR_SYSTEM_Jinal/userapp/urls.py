from django.conf.urls import url
from userapp import views

urlpatterns = [
    url(r'^$',views.display_movies),
    url(r'^see_ratings/$',views.calculate_rating),
]