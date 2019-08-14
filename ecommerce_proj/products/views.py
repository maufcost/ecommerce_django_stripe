from .models import Product
from cart.models import Cart
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

def home(request):
    return render(request, "products/home.html")

def about(request):
    # Just playing with django sessions ----------------------------------------
    # print(request.session.get("first_name", "Unknown"))
    # --------------------------------------------------------------------------
    return render(request, "products/about.html")

class ProductListView(ListView):
    model = Product
    template_name = "templates/product_list.html"

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        # Overwriting 'get_context_data' from the parent class to add additional
        # context (in this case the cart object for the current user).
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        # Checks if a product exists for the given slug in the url and
        # retrieves the product from db (if one exists for the given slug).
        request = self.request
        slug = self.kwargs.get("slugstring") # 'slugstring' is the name of the get param we set at urls.py.
        try:
            instance = Product.objects.get(slug=slug)
            return instance
        except Product.DoesNotExist:
            raise Http404("This product doesn't exist!")
