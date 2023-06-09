from django.db import models
from django.utils import timezone

from django.conf import settings
import uuid


from django.contrib.auth.models import AbstractUser

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default= timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.title

