from django.db import models

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    audio_path = models.TextField()
    image = models.ImageField(null=True , default=None , upload_to = 'post_pics')
# Create your models here.
