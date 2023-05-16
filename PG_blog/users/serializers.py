from .models import NewUser,Profile
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers



class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image_url','make_thumbnail']   


class UserSerializer(ModelSerializer):
    # post_count = SerializerMethodField(read_only=True)
    profile=ProfileSerializer()
    class Meta:
        model = NewUser
        fields = ['id','username','email','age','nickname','profile']

        # def get_post_count(self,obj):
        #     count = obj..count()
        #     return count

  