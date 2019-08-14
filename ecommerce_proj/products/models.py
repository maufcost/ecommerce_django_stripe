from django.db import models
from django.db.models import Q
from django.urls import reverse
from ecommerce_proj.utils import unique_slug_generator
from django.db.models.signals import pre_save

class ProductManager(models.Manager):
    def get_by_id(self, id):
        # Returns a product based on a product id.
        query_set = self.get_queryset().filter(id=id)
        if query_set.count() == 1:
            return query_set.first()
        return None

    def search(self, query):
        # Returns product(s) based on a particular query string 'query.'
        lookups = Q(title__contains=query) | Q(description__contains=query) | Q(tag__title__contains=query)
        return self.get_queryset().filter(lookups).distinct()

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(default="default.jpg", upload_to="products")
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True) # Set when saved to db.

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product-detail-upn", kwargs={"slugstring":self.slug})

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
