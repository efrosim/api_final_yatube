from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']

        if user == following:
            raise ValidationError("Нельзя подписаться на самого себя!")

        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя!")

        return data

    class Meta:
        fields = '__all__'
        model = Follow
