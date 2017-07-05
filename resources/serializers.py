from rest_framework import serializers

from users.serializers import UserReadSerializer
from .models import Category, Resource, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = UserReadSerializer(read_only=True)


    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'posted_on')
        read_only_fields = ('id',)

    def create(self, validated_data):
        request = self.context['request']
        resource = self.context['resource']

        return Comment.objects.create(resource=resource, author=request.user, **validated_data)


class ResourceSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    owner = UserReadSerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True, many=True)


    class Meta:
        model = Resource
        fields = ('id', 'title', 'categories', 'resource_url', 'owner', 'comment_set')
        read_only_fields = ('id',)

    def create(self, validated_data):
        request = self.context['request']

        return Resource.objects.create(owner=request.user, **validated_data)
