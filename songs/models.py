from django.db import models
from django.urls import reverse
from PIL import Image

class Song(models.Model):
    title = models.CharField(max_length=100)
    lyrics = models.TextField()
    composer = models.CharField(max_length=100)
    featuring = models.TextField(blank=True)
    album = models.CharField(max_length=100)
    img = models.ImageField(upload_to='cover_pic/')
    link =  models.CharField(max_length=1000)  # embed link
    ytlink = models.CharField(max_length=1000 ,default='')
    genre = models.CharField(max_length=100,blank=True)
    audio = models.FileField(upload_to='audio/',default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-details',kwargs={'pk': self.pk})

    def save(self):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image = image.resize(output_size)
            image.save(self.img.path)
