from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.files import File
from PIL import Image
from io import BytesIO
# Create your models here.


class NewUser(AbstractUser):
    age = models.IntegerField(null=True,blank=True)
    nickname = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.username
    

class Profile(models.Model):
    user = models.OneToOneField(NewUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def image_url(self):
        return f'http://localhost:8000{self.image.url}'
    
    def make_thumbnail(self):
        img = Image.open(self.image)
        img.convert('RGB') 
        img.thumbnail(size=(300,200))
        
        thumb_io = BytesIO()
        img.save(thumb_io,'png',quality=85)

        thumbnail = File(thumb_io,name=self.image.name)
        return f'http://localhost:8000/media/{thumbnail.name}'