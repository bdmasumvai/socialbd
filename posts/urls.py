from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('post/comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
