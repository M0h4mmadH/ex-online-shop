from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shop/', include('apps.shop.urls')),
    path('api/v1/users/', include('apps.user.urls')),
]
