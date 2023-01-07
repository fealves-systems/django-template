from django.urls import path
from accounts.views import *

app_name = "accounts" 

urlpatterns = [
    path("adicionar/", AddUser, name="add_user"),
    path("login/", LoginUser, name="login"),
    path("logout/", LogoutUser, name="logout"),
]


