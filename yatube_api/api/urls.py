from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()
v1_router.register('posts', views.PostViewSet)
v1_router.register('groups', views.GroupViewSet)
v1_router.register('follow', views.FollowViewSet, basename='follow')
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments', 
    views.CommentViewSet, 
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
