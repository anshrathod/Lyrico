from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/' ,default='default.png', null=True)
    bio = models.TextField(blank=True)
    age = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user)

    def saave(self):
        super().save()
        print('tp')
        img = Image.open(self.image.path)
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)