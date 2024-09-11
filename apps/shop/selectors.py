from django.db import transaction
from django.db.models import Q

from apps.shop.models import (Product, ProductCategory, Cart, CartItem, PurchaseReceipt)


def search_products(validated_data):
    search = validated_data.get('search', '')
    category = validated_data.get('category', '')
    min_price = validated_data.get('min_price')
    max_price = validated_data.get('max_price')
    city = validated_data.get('city')
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

    if city is not None:
        queryset = queryset.filter(city__name__icontains=city)

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


def update_product(validated_data):
    product = Product.objects.get(id=validated_data['id'])
    for attr, value in validated_data.items():
        setattr(product, attr, value)
    product.save()
    return product


def create_category(validated_data):
    return ProductCategory.objects.create(**validated_data)


def update_category(validated_data):
    category = ProductCategory.objects.get(name=validated_data['current_name'])
    if 'new_name' in validated_data:
        category.name = validated_data['new_name']
    if 'is_active' in validated_data:
        category.is_active = validated_data['is_active']
    category.save()
    return category


def get_or_create_active_cart(user):
    cart, created = Cart.objects.get_or_create(
        user=user,
        cart_status='O',
        is_active=True,
        defaults={'cart_status': 'O'}
    )
    return cart


def add_item_to_cart(cart, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    return cart_item


@transaction.atomic
def process_add_items_to_cart(user, items_data):
    cart = get_or_create_active_cart(user)
    cart_items = []
    for item_data in items_data:
        cart_item = add_item_to_cart(cart, item_data['product_id'], item_data['quantity'])
        cart_items.append(cart_item)
    return cart, cart_items


def get_user_purchase_receipts(user, **filters):
    return PurchaseReceipt.objects.filter(user=user)


def get_user_open_carts(user, **filters):
    return Cart.objects.filter(user=user, cart_status='O')
