from django.conf.urls import url

from .views import UserLogin


app_name = 'users'

urlpatterns = [
    url(r'^login/', UserLogin.as_view(), name='login')
]
