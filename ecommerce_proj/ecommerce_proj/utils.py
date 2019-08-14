import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    # Generates a random string of size 'size' with characters 'chars.'
    return "".join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
    # Generates a random unique string to be the id of an order. The 'instance'
    # model should have a slug field.
    new_order_id = random_string_generator()
    klass = instance.__class__
    qs_exists = klass.objects.get(order_id=new_order_id)
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id

def unique_slug_generator(instance, new_slug=None):
    # Generates unique slugs for a particular 'instance.' The 'instance' model
    # should have a slug field.
    slug = None
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        # An instance with the generated slug already exists.
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)
    # An instance with the generated slug does not exist yet.
    return slug
