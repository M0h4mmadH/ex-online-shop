from django.urls import path
from apps.shop.views import *

urlpatterns = [
    path('products/', GetProducts.as_view(), name='search products'),
    path('categories/', GetCategories.as_view(), name='search categories'),
    path('products/create', AdminCreateProducts.as_view(), name='admin create products'),
    path('products/update', AdminUpdateProducts.as_view(), name='admin update products'),
]
