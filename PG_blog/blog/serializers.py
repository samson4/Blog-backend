from .models import Post

from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from django.contrib.auth.models import User
from users.serializers import UserSerializer

class PostSerializer(ModelSerializer):
    author = UserSerializer() 
    
    class Meta:
        model = Post
        fields = ['id','title','content','date_posted','author']

       


