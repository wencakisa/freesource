from rest_framework import permissions


class IsResourceOwner(permissions.BasePermission):
    message = 'You are not the resource owner.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsCommentAuthor(permissions.BasePermission):
    message = 'You can delete only your own comments.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
