from django.urls import path
from apps.shop.views import *

urlpatterns = [
    path('products/', GetProducts.as_view(), name='search products'),
    path('categories/', GetCategories.as_view(), name='search categories'),
]
