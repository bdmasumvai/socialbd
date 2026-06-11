from django.urls import path
from . import views

urlpatterns = [
    path('send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept/<int:user_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/<int:user_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),
    path('requests/', views.friend_requests_view, name='friend_requests'),
]
