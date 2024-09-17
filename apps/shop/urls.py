from django.urls import path
from apps.shop.views import *

urlpatterns = [
    path('products/', GetProducts.as_view(), name='search products'),
    path('categories/', GetCategories.as_view(), name='search categories'),
    path('products/create/', AdminCreateProducts.as_view(), name='admin create products'),
    path('products/update/', AdminUpdateProducts.as_view(), name='admin update products'),
    path('categories/create/', AdminCreateCategory.as_view(), name='admin create categories'),
    path('categories/update/', AdminUpdateCategory.as_view(), name='admin update categories'),
    path('cart/add-items/', UserAddItemsToCart.as_view(), name='user add items to cart'),
    path('cart/delete/', UserDeleteCart.as_view(), name='user delete cart'),
    path('user/get-purchases/', GetUserPurchaseReceipts.as_view(), name='user get purchase'),
    path('user/get-active-carts/', GetUserActiveCarts.as_view(), name='user get carts'),
    path('product/comment/', UserCommentProducts.as_view(), name='user comment product'),
    path('product/rate', UserRateProducts.as_view(), name='user rate product'),
    path('user/address/create', UserAddAddress.as_view(), name='user create address'),
    path('user/address/update', UserUpdateAddress.as_view(), name='user update address'),
    path('user/address/delete', UserDeleteAddress.as_view(), name='user delete address'),
    path('user/address/get', UserGetAddress.as_view(), name='user get address'),
    path('cart/purchase', UserPurchaseCart.as_view(), name='user purchase cart'),
]
