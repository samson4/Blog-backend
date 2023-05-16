from django.urls import path,include


from . import views

urlpatterns = [
      
      path('register/',views.Register.as_view(),name='user-register'),
      path('profile/',views.UserProfile.as_view(),name="user-profile"),
  
]