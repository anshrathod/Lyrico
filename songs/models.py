from django.db import models
from django.urls import reverse

class Song(models.Model):
    title = models.CharField(max_length=100)
    lyrics = models.TextField()
    composer = models.CharField(max_length=100)
    featuring = models.TextField()
    album = models.CharField(max_length=100)
    img = models.ImageField(default='default.jpg',upload_to='')
    link =  models.CharField(max_length=1000)  # embed link
    ytlink = models.CharField(max_length=1000 ,default='')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-details',kwargs={'pk': self.pk})
