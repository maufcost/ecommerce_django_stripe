from django.urls import path, re_path
from . import views

# 'upn' stands for "url pattern."
urlpatterns = [
    path("", views.home, name="home-upn"),
    path("about/", views.about, name="about-upn"),
    path("list/", views.ProductListView.as_view(), name="product-list-upn"),
    # 'slug' is the type. 'slugstring' is the actual GET parameter value.
    path("<slug:slugstring>/", views.ProductDetailView.as_view(), name="product-detail-upn"),

    # Not implemented yet:
    # path("create/", views.ProductCreateView.as_view(), name="product-create-upn"),
    # path("update/<int:pk>/", views.ProductUpdateView.as_view(), name="product-update-upn"),
    # path("delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product-delete-upn"),
]
