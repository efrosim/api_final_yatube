from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        # Если не указаны параметры пагинации, возвращаем список без пагинации
        if ('limit' not in request.query_params
                and 'offset' not in request.query_params):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Иначе используем стандартную пагинацию
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = None
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
