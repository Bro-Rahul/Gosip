from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

routers = DefaultRouter()
routers.register('users-forget-password',views.ForgetPasswordView,basename="sdasd")   
routers.register('users',views.ValidateEmailCodeView,basename='generate-unique-code')
routers.register('users',views.UserView,basename='dsadd')
routers.register('users',views.SecretKeyView,basename='secret-key')

urlpatterns = [
    path('',include(routers.urls)),
    path('auth/',views.AuthenticationView.as_view()),
    path('auth/user/<int:pk>/logout-user',views.AuthenticationView.as_view()),
]
