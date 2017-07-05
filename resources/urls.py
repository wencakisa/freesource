from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import CategoryListView, ResourceCategoryList, ResourceViewSet, CommentViewSet


app_name = 'resources'

urlpatterns = [
    url(r'^categories/$', CategoryListView.as_view(), name='category-list'),
    url(
        r'^resources/(?P<category_name>[a-z]+)/$',
        ResourceCategoryList.as_view(),
        name='resource-category-list'
    )
]

resource_router = routers.DefaultRouter()
resource_router.register(r'resources', ResourceViewSet, base_name='resources')

resource_comments_router = nested_routers.NestedDefaultRouter(
    resource_router, r'resources', lookup='resource'
)
resource_comments_router.register(
    r'comments', CommentViewSet, base_name='resource-comments'
)

urlpatterns += resource_router.urls
urlpatterns += resource_comments_router.urls
