from django.urls import path,include


from . import views

urlpatterns = [
      
      path('register/',views.Register.as_view(),name='user-register'),
      path('delete/<int:id>/', views.DeleteUser.as_view(), name='user-delete'),
      path('profile/',views.UserProfile.as_view(),name="user-profile"),
      # path('verifytoken/',views.JWTAutentication.as_view()),
  
]