from django.urls import path,include


from . import views

urlpatterns = [
      path('',views.home,name='blog-home'),
      path('about/',views.about,name='blog-about'),
      path('post/<int:pk>/',views.PostDetail.as_view(),name='post-detail'),
      path('post/new/',views.PostCreate.as_view(),name='post-create'),
      path('post/<int:pk>/update/',views.PostUpdate.as_view(),name='post-update'),
      path('post/<int:pk>/delete/',views.PostDelete.as_view(),name='post-delete')
]