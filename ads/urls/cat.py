from django.contrib import admin
from django.urls import path
from rest_framework import routers

from ads.views.cat import CategoryViewSet

"""urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('create/', CategoryCreateView.as_view()),
    path('<int:pk>/update/', CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryDeleteView.as_view()),
]"""

router = routers.SimpleRouter()
router.register('', CategoryViewSet)

urlpatterns = router.urls