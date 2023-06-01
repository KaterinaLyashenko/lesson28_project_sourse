from django.urls import path
from rest_framework import routers

from users.views import UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserListView

urlpatterns = [
    path('', UserListView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
]

