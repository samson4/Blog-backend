from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser

from users.models import NewUser,Profile
from.serializers import UserSerializer,ProfileSerializer,TokenSerializer

# from .models import Post
# from .serializers import PostSerializer
# Create your views here.
class Register(APIView):

    def get(self,request):
        queryset = NewUser.objects.all()
        serializer = UserSerializer(queryset,many=True)

        return Response(serializer.data) 
       
    def post(self,request):
        username = request.data['username']
        email =request.data['email']
        password=request.data['password']
        try:
            existingUser = NewUser.objects.get(username=username)
            if existingUser:
                return Response("Duplicate User already exists")
        except:
            queryset = NewUser.objects.create_user(username = username,email = email,password = password)
            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        # if NewUser.objects.get(username=username):
        #     return Response("Duplicate User already exists")
        # else:
        #     queryset = NewUser.objects.create_user(username = username,email = email,password = password)
        #     serializer = UserSerializer(queryset)
        #     return Response(serializer.data)

class UserProfile(APIView):
    permission_classes=[IsAuthenticated]
    # parser_classes=[FormParser]
    def get_object(self,username):
        try:
            return NewUser.objects.get(username=username)
        except NewUser.DoesNotExist:
            raise Http404
        
    def get(self,request):
        queryset = self.get_object(request.user)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)
    
    def put(self,request):
        try:
            queryset = self.get_object(request.user)
            username = request.data['username']
            email = request.data['email']
            age = request.data['age']
            nickname = request.data['nickname']
            image = request.data['image']
            queryset.username = username
            queryset.email = email
            queryset.age = age
            queryset.profile.image = image
            print(image)
            queryset.nickname = nickname
            
            queryset.save()
            print(queryset.profile.image)

            serializer = UserSerializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            print(e)
        


# from rest_framework_simplejwt.authentication import JWTAuthentication
# JWT_authenticator = JWTAuthentication()    
# class JWTAutentication(APIView):

#     def post(self,request):
#         print(JWT_authenticator.get_validated_token(request))
#         response = JWT_authenticator.authenticate(request)
#         user,*info = response
#         print((info))
        
#         # for i in json.dumps(tuple(args)):
#         # # if 'user_id' in args:
#         #     print(json.dumps(tuple(args)))
#         # else:
#         #     print('False')    
#         return Response(user)

   
        