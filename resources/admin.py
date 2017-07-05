from django.contrib import admin

from .models import Category, Resource


class ResourceAdmin(admin.ModelAdmin):
    fields = ('title', 'categories', 'resource_url', 'owner')


admin.site.register(Category)
admin.site.register(Resource, ResourceAdmin)
