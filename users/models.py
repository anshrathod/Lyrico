from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    GENDER_CHOICES=[
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/' ,default='default.png', null=True)
    bio = models.TextField(blank=True)
    age = models.IntegerField(blank=True,default=0)
    gender = models.CharField(max_length=10)

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)