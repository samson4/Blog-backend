import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory,force_authenticate
from .models import NewUser
from .serializers import UserSerializer
from .views import Register,UserProfile
from collections import OrderedDict
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = Register.as_view()
        self.url = reverse('user-register')
        self.test_user = NewUser.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        

    def test_get_all_users(self):
        url = reverse('user-register')
        request = self.factory.get(url)
        response = self.view(request)
        
        # check that the response status code is 200 OK
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        test_serializer = UserSerializer([self.test_user], many=True)
        response_serializer = UserSerializer(response.data,many=True)
        # print(test_serializer.data)
        # print(response_serializer.data)

        #check the test_user data is the same as get_user response data
        self.assertEqual(test_serializer.data,response_serializer.data)


    def test_create_new_user(self):
        # simulate a POST request to the view with valid data
        valid_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass'}
        url = reverse('user-register')
        request = self.factory.post(url,valid_data)
        response = self.view(request)
        # print(response.data)

        # check that the response status code is 201 Created
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        # check that the response data matches the expected output
        serializer = UserSerializer(response.data)
        expected_output = {'id':3,'username': 'newuser', 'email': 'newuser@example.com', 'age':None, 'nickname':None,'profile':{'image_url': 'http://localhost:8000/media/default.jpg', 'make_thumbnail': 'http://localhost:8000/media/default.jpg'}}
        
        self.assertEqual(serializer.data,expected_output)

        # check that the new user has been created in the database
        new_user = NewUser.objects.filter(username='newuser').first()
        self.assertIsNotNone(new_user)

    def test_create_duplicate_user(self):
        # simulate a POST request to the view with a duplicate username
        invalid_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpass'}  
        register_url =self.url 
        request = self.factory.post(register_url,invalid_data)
        response = self.view(request) 

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        # print(response.data)


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.factory =  APIRequestFactory()
        self.view = UserProfile.as_view()
        
        self.url = reverse("user-profile")
        self.test_user = NewUser.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    def test_profile_get_all_users(self):
    

        # Obtain Token for authentication
        loginurl = reverse("token_obtain_pair")
        data = {
        'username': 'testuser',
        'password': 'testpass'
                }
        
        login_request = self.factory.post("/api/token/",data)
        view = TokenObtainPairView.as_view()
        res=view(login_request)
        token = res.data['access']

        
        # Simulate a get request for user profile
        request = self.factory.get(self.url)
        force_authenticate(request,user=self.test_user,token=token)
        response = self.view(request)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        expected_output = {'id':5,'username': 'testuser', 'email': 'test@example.com', 'age':None, 'nickname':None,'profile':{'image_url': 'http://localhost:8000/media/default.jpg', 'make_thumbnail': 'http://localhost:8000/media/default.jpg'}}
        self.assertEqual(response.data,expected_output)
        

# class RegisterViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.view = Register.as_view()
        
#         # create a test user for use in the tests
#         self.test_user = NewUser.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        
#     def test_get_all_users(self):
#         # simulate a GET request to the view
#         request = self.factory.get('/register/')
#         response = self.view(request)
        
#         # check that the response status code is 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # check that the response data contains the test user
#         serializer = UserSerializer([self.test_user], many=True)
#         self.assertEqual(response.data, serializer.data)
        
#     def test_create_new_user(self):
#         # simulate a POST request to the view with valid data
#         valid_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass'}
#         request = self.factory.post('/register/', valid_data)
#         response = self.view(request)
        
#         # check that the response status code is 201 Created
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # check that the response data matches the expected output
#         expected_output = {'id': 3, 'username': 'newuser', 'email': 'newuser@example.com', 'age': None, 'nickname': None}
#         self.assertEqual(response.data, expected_output)
        
#         # check that the new user has been created in the database
#         new_user = NewUser.objects.filter(username='newuser').first()
#         self.assertIsNotNone(new_user)
        
#     def test_create_duplicate_user(self):
#         # simulate a POST request to the view with a duplicate username
#         invalid_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpass'}
#         request = self.factory.post('/register/', invalid_data)
#         response = self.view(request)
        
#         # check that the response status code is 400 Bad Request
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
#         # check that the response data contains the error message
#         self.assertEqual(response.data, 'Duplicate User already exists')