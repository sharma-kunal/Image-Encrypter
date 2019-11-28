# pages/urls.py
from django.urls import path

from .views import homePageView, encrypt, decrypt

urlpatterns = [
    path('', homePageView, name='home'),
    path(r'encrypt', encrypt),
    path(r'decrypt', decrypt),
]