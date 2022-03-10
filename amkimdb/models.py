import datetime

from django.db import models

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length = 100)
    released_year = models.CharField(max_length = 10)
    image = models.URLField()

    @property
    def movie_comments(self):
        return self.comments.all()


    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.CharField(max_length = 100)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)
    movie = models.ForeignKey(Movie, blank=True, on_delete=models.CASCADE, related_name='comments', null=True)

    def __str__(self):
        return f"MOVIE: {self.movie} USER: {self.user} DATE: {self.date}"