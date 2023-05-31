from django.urls import path
from rest_framework import routers

from users.serializers import LocationSerializer
from users.views import UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserListView, LocationViewSet

router = routers.SimpleRouter()
router.register('', LocationViewSet)

urlpatterns = router.urls