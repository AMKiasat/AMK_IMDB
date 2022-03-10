from django.shortcuts import render

from amkimdb import models


def home_page(request):
    movies = models.Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})


def language_page(request, movie_id):
    return render(request, 'index2.html', {'movie_id': movie_id})


def comment_page(request, movie_id):
    comments = models.Movie.objects.get(id=movie_id).movie_comments
    return render(request, 'index3.html', {'comments': comments})
