from django.contrib import admin
from django.urls import path, include
from users.views import LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', LoginAPI.as_view()),
    path('api/posts/', include('posts.urls')),
    path('api/users/', include('users.urls')),
]
