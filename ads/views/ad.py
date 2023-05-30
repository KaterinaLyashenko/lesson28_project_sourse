import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from users.models import User

TOTAL_ON_PAGE = 5

class AdListView(ListView):
    queryset = Ad.objects.order_by("-price")
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        ads_on_page = paginator.get_page(page_number)

        return JsonResponse({
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "items": [ad.serialize() for ad in ads_on_page]},
            safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, pk=data.pop("author_id"))
        category = get_object_or_404(Category, pk=data.pop("category"))

        new_category = Ad.objects.create(author=author, category=category, **data)
        return JsonResponse(new_category.serialize())

class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())

@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if 'name' in ad_data:
            self.object.name = ad_data['name']
        if 'author_id' in ad_data:
            author = get_object_or_404(User, pk=ad_data['author_id'])
            self.object.author = author
        if 'price' in ad_data:
            self.object.price = ad_data['price']
        if 'is_published' in ad_data:
            self.object.is_published = ad_data['is_published']
        if 'category_id' in ad_data:
            category = get_object_or_404(Category, pk=ad_data['author_id'])
            self.object.category = category

        self.object.save()
        return JsonResponse(
            {
                'id': self.object.id,
                'name': self.object.name,
                'author': self.object.author.username,
                'price': self.object.price,
                'description': self.object.description,
                "address": [loc.name for loc in self.object.author.locations.all()],
                'is_published': self.object.is_published,
                'category': self.object.category.name
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = "__all__"
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse(self.get_object().serialize())