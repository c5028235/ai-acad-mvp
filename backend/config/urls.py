from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from academy.views import RegisterView
urlpatterns=[path('admin/',admin.site.urls),path('api/auth/register/',RegisterView.as_view()),path('api/auth/login/',TokenObtainPairView.as_view()),path('api/auth/refresh/',TokenRefreshView.as_view()),path('api/',include('academy.urls'))]
