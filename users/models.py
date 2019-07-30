from django.db import models
from django.contrib.auth.models import User
from songs.models import Song

class Profile(models.Model):
    GENDER_CHOICES=[
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/')
    bio = models.TextField(blank=True)
    age = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user } Profile' 