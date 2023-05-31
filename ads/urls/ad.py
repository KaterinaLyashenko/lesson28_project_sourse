from django.contrib import admin
from django.urls import path
from rest_framework import routers

from ads.views.ad import AdViewSet, AdUploadImageView

router = routers.SimpleRouter()
router.register('', AdViewSet)

urlpatterns = [
    #path('', AdListSerializer.as_view()),
    #path('create/', AdCreateView.as_view()),
    #path('<int:pk>/', AdDetailView.as_view()),
    #path('<int:pk>/update/', AdUpdateView.as_view()),
    #path('<int:pk>/delete/', AdDeleteView.as_view()),
    path('<int:pk>/upload/', AdUploadImageView.as_view()),

]

urlpatterns += router.urls