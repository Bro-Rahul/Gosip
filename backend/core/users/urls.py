from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

routers = DefaultRouter()
routers.register('users',views.UserView)
routers.register('users',views.SecretKeyView,basename='secret-key')

urlpatterns = [
    path('',include(routers.urls)),
    path('auth/',views.AuthenticationView.as_view()),
    path('auth/user/<int:pk>/logout-user',views.AuthenticationView.as_view()),
]
