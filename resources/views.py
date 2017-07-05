from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from .models import Category, Resource
from .serializers import CategorySerializer, ResourceSerializer, CommentSerializer
from .permissions import IsResourceOwner, IsCommentAuthor


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'get': (IsAuthenticated,),
        'post': (IsAuthenticated, IsAdminUser)
    }
    queryset = Category.objects.all()

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.request.method.lower()]
        ]


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
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'update': (IsAuthenticated, IsResourceOwner),
        'destroy': (IsAuthenticated, IsResourceOwner)
    }
    queryset = Resource.objects.all()

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def create(self, request):
        context = {'request': request}

        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None):
        resource = get_object_or_404(Resource, id=pk)
        self.check_object_permissions(request, resource)

        serializer = self.get_serializer(resource, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'create': (IsAuthenticated,),
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'update': (IsAuthenticated, IsCommentAuthor),
        'destroy': (IsAuthenticated, IsCommentAuthor)
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

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
