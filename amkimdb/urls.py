from django.urls import path, include

from amkimdb import views

urlpatterns = [
    path('', views.home_page),
]