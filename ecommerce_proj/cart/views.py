from .models import Cart
from products.models import Product
from django.shortcuts import render, redirect

def cart_home(request):
    # Playing with Django sessions ---------------------------------------------
    # print(request.session) # A django session object.
    # print(dir(request.session)) # All the different methods you can apply with
    # this object. 'dir' is built-in.
    # print(request.session.session_key)
    # print(request.session.set_expiry(300)) # Makes the session expire after 5 min.
    # request.session["first_name"] = "Justin"
    # --------------------------------------------------------------------------

    # Getting a reference to this user's cart.
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "cart/cart_home.html", {"cart":cart_obj})

def cart_update(request):
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            # Getting a reference to the product (if any).
            product_obj = Product.objects.get(id=int(product_id)) # Raises.

            # Getting a reference to the cart.
            cart_obj, new_obj = Cart.objects.new_or_get(request)

            if product_obj in cart_obj.products.all():
                # The product is already in the cart, so let's remove it.
                cart_obj.products.remove(product_obj)
            else:
                # The product is not in the cart, let's add it.
                cart_obj.products.add(product_obj)

            request.session["cart_num_items"] = cart_obj.products.count()
            return redirect(product_obj.get_absolute_url())

        except Product.DoesNotExist:
            return redirect("cart-home-upn")

# Note: Notice that we're not running the 'save()' method after the remove and
# add operations in the 'cart_update' view. It is because we're dealing with
# a ManyToMany field. The 'save' method is handled in the M2M method in the models
# file.
