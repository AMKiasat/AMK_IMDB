from django.shortcuts import render

from amkimdb import models


def home_page(request):
    movies = models.Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})
