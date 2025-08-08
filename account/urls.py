from django.urls import path
from .views import *

app_name = 'account'

urlpatterns=[
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', register_page, name='register'),
    path('logout/', log_out, name='logout'),
    path('profile/', profile, name='profile'),
]