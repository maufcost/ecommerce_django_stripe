from products.models import Product
from django.shortcuts import render
from django.views.generic import ListView

class SearchProductListView(ListView):
    model = Product
    template_name = "search/search_list.html"

    def get_queryset(self, *args, **kwargs):
        # Queries the objects to be shown in this list view.
        request = self.request
        query_word = request.GET.get("q")
        if query_word is not None:
            return Product.objects.search(query_word)
            # return Product.objects.filter(title__contains=query_word) # old.
        return Product.objects.all()
