from django.db.models import Q

from apps.shop.models import (Product, Order, ProductCategory)


def search_products(validated_data):
    search = validated_data.get('search', '')
    category = validated_data.get('category', '')
    min_price = validated_data.get('min_price')
    max_price = validated_data.get('max_price')
    order_by = validated_data.get('order_by', 'name')

    queryset = Product.objects.filter(is_active=True)

    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

    if category:
        queryset = queryset.filter(category__name=category)

    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)

    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)

    queryset = queryset.order_by(order_by)
    return queryset


def search_categories(validated_data):
    search = validated_data.get('search', '')
    order_by = validated_data.get('order_by', 'name')

    queryset = ProductCategory.objects.filter(is_active=True)

    if search:
        queryset = queryset.filter(name__icontains=search)

    queryset = queryset.order_by(order_by)
    return queryset


def create_product(validated_data):
    return Product.objects.create(**validated_data)


def update_product(product_id, validated_data):
    product = Product.objects.get(id=product_id)
    for attr, value in validated_data.items():
        setattr(product, attr, value)
    product.save()
    return product


def generate_purchase_order_factor(order: Order):
    pass
