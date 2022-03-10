from django.urls import path, include

from amkimdb import views

urlpatterns = [
    path('', views.home_page),
    path('<int:movie_id>/language', views.language_page),
    # path('<int:movie_id>/comments/<int:language>', views.comment_page),
    path('<int:movie_id>/comments', views.comment_page),
]