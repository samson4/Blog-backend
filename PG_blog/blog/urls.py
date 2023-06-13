from django.urls import path,include


from . import views

urlpatterns = [
      path('',views.Home.as_view(),name='blog-home'),
      path('post/<int:pk>/',views.PostDetail.as_view(),name='post-detail'),
      path('post/new/',views.PostCreate.as_view(),name='post-create'),
      path('post/<int:pk>/update/',views.PostUpdate.as_view(),name='post-update'),
      path('post/<int:pk>/delete/',views.PostDelete.as_view(),name='post-delete'),
      path('post/user/<str:username>/',views.UserPosts.as_view(),name='user-posts'),
      path('post/',views.SearchPosts.as_view(),name='search-posts')
      
]