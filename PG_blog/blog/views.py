from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


from .models import Post
from .serializers import PostSerializer
# Create your views here.


class Home(APIView,PageNumberPagination):
    page_size=2
    def get(self,request):
        
        query = Post.objects.all().order_by("-date_posted")
        result = self.paginate_queryset(query,request,view=self)
        serializer = PostSerializer(result,many=True)
        return self.get_paginated_response(serializer.data)

# @api_view(['GET'])
# def home(request):
#     pagination_class = PageNumberPagination
#     query = Post.objects.all().order_by("-date_posted")
#     serializer = PostSerializer(query,many=True)
    
#     return Response(serializer.data)


class PostDetail(APIView):
    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
            
        except Post.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        queryset =self.get_object(pk)
        serializer = PostSerializer(queryset)
        
        print(request.user)
        return Response(serializer.data)

class PostCreate(APIView):
     
     def post(self,request):
         title = request.data['title']
         content = request.data['content']
         user = request.user

         try:
             NewPost = Post.objects.create(title=title,content=content,author=user)
             serializer = PostSerializer(NewPost)
             return Response(serializer.data)
         except:
             print('error')


class PostUpdate(APIView):

    permission_classes=[IsAuthenticated]

    def get_object(self,pk,user):
       
        try:
            return Post.objects.get(pk=pk,author=user)
        except Post.DoesNotExist:
            raise Http404

    def put(self,request,pk): 
        queryset = self.get_object(pk,request.user)  
        title = request.data['title']
        content=request.data['content']  
        queryset.title = title
        queryset.content = content
        queryset.save()
        serializer = PostSerializer(queryset)
        return Response(serializer.data)
    

class PostDelete(APIView):

    permission_classes=[IsAuthenticated]

    def get_object(self,pk,user):
        try:
            return Post.objects.get(pk=pk,author=user)
        except Post.DoesNotExist:
            raise Http404 
        
    def delete(self,request,pk):
        user = request.user
        try:
            queryset = self.get_object(pk,user)
            queryset.delete()
            # serializer = PostSerializer(queryset)
            
            return Response('delete successful') 
        except Exception as e:
            return Response({'Error':str(e)}) 
