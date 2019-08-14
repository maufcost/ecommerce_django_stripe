from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

class CartManager(models.Manager):

    def new_or_get(self, request):
        # Returns an existing cart or creates a new one and returns it.
        cart_obj, new_obj = None, None
        cart_id = request.session.get("cart_id", None)
        if cart_id is None:
            # There isn't a cart id in the session. Let's associate one and create
            # a new cart.
            cart_obj = self.create_new_cart(request.user)
            request.session["cart_id"] = cart_obj.id
            new_obj = True
        else:
            # There is a cart id in the session. Let's retrieve that cart.
            cart_obj = self.get_queryset().get(id=cart_id)
            if request.user.is_authenticated and cart_obj.user is None:
                # Associating an already created cart with a user that just logged in.
                # That way, we will associate the same cart id for the just logged in
                # user as the cart id he had when he wasn't logged in (preventing him
                # from losing the products in his cart now that he has an account).
                cart_obj.user = request.user
                cart_obj.save()
                new_obj = False
            else:
                # The user who logged in already has a cart associated with it.
                pass
        return cart_obj, new_obj

    def create_new_cart(self, user=None):
        # Creates new cart.
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) # I believe, I could've used a OneToOneField here.
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def cart_update_receiver(sender, instance, action, *args, **kwargs):
    # Calculates the total amount of the cart.
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        total = 0
        for product in instance.products.all():
            total += product.price
        instance.total = total
        instance.save() # We need to save it manually (this is not a conventional signal)

m2m_changed.connect(cart_update_receiver, sender=Cart.products.through)
