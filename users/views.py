import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    CreateAPIView
from rest_framework.viewsets import ModelViewSet

from avito import settings
from users.models import User, Location
from users.serializers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer, LocationSerializer


class UserListView(ListAPIView):
    queryset = User.objects.prefetch_related("locations").annotate(
        total_ads=Count('ad', filter=Q(ad__is_published=True))).order_by("username")
    serializer_class = UserListSerializer

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

