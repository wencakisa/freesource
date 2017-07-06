from django.conf.urls import url

from .views import UserRegister, UserLogin


app_name = 'users'

urlpatterns = [
    url(r'^register/', UserRegister.as_view(), name='register'),
    url(r'^login/', UserLogin.as_view(), name='login')
]
