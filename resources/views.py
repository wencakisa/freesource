from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Category, Resource
from .serializers import CategorySerializer, ResourceSerializer, CommentSerializer


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()


class ResourceCategoryList(generics.ListAPIView):
    serializer_class = ResourceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        category_name = self.kwargs.get('category_name').title()
        category = get_object_or_404(Category, name=category_name)

        return Resource.objects.filter(categories__in=[category])


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Resource.objects.all()

    def create(self, request):
        context = {'request': request}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        resource_pk = self.kwargs.get('resource_pk')
        resource = get_object_or_404(Resource, id=resource_pk)

        return resource.comment_set

    def create(self, request, resource_pk=None):
        resource = get_object_or_404(Resource, id=resource_pk)

        context = {'request': request, 'resource': resource}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)