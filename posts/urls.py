from django.urls import path
from . import views

urlpatterns = [
    path('news-posts/', views.PostAPIView.as_view()),
    path('comments/', views.CommentAPIView.as_view()),
]