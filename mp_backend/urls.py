
from django.contrib import admin
from django.urls import path, include
from users.views import RegisterView, LoginView




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    
    
]
