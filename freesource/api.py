from django.conf.urls import url, include

urlpatterns = [
    url('', include('users.urls')),
    url('', include('resources.urls')),
]
