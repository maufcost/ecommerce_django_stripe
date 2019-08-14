from django.urls import path
from search.views import SearchProductListView

urlpatterns = [
    path("list/", SearchProductListView.as_view(), name="search-product-list-upn"),
]
