from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

routers = DefaultRouter()
routers.register('posts',views.ThreadView)
routers.register('posts-comment',views.CommentView)
routers.register('comment',views.CommentLikeDislikeView)

urlpatterns = [
    path('',include(routers.urls))
]
