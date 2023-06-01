import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from ads.serializer import AdListSerializer, AdSerializer, AdDetailSerializer

class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by("-price")
    serializers = {"list": AdListSerializer, "retrieve": AdDetailSerializer}
    default_serializer = AdSerializer

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        cat_list = request.GET.getlist("cat")
        if cat_list:
            self.queryset = self.queryset.filter(category_id__in=cat_list)

        text = request.GET.getlist("text")
        if text:
            self.queryset = self.queryset.filter(name__incontains=text)

        locations = request.GET.getlist("locations")
        if locations:
            self.queryset = self.queryset.filter(author__locations__name__icontains=locations)

        price_from = request.GET.getlist("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.getlist("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = "__all__"
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse(self.get_object().serialize())