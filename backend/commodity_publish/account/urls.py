from django.urls import include, path
from .views import *

urlpatterns = [
    path("user/<str:pk>", UserDetail.as_view()),
    path("users", UserList.as_view()),
]