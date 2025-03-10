from django.db import transaction
from django.db.models import Q, Sum

from apps.shop.models import (Product, ProductCategory, Cart, CartItem, PurchaseReceipt)
from apps.utils.exceptions import TooManyItemsException


def search_products(validated_data):
    search = validated_data.get('search', '')
    category = validated_data.get('category', '')
    min_price = validated_data.get('min_price')
    max_price = validated_data.get('max_price')
    city = validated_data.get('city')
    order_by = validated_data.get('order_by', 'name')

    queryset = Product.active.filter(is_active=True)

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

    queryset = ProductCategory.active.filter(is_active=True)

    if search:
        queryset = queryset.filter(name__icontains=search)

    queryset = queryset.order_by(order_by)
    return queryset


def create_product(validated_data):
    return Product.active.create(**validated_data)


def update_product(validated_data):
    product = Product.active.get(id=validated_data['id'])
    for attr, value in validated_data.items():
        setattr(product, attr, value)
    product.save()
    return product


def create_category(validated_data):
    return ProductCategory.active.create(**validated_data)


def update_category(validated_data):
    category = ProductCategory.active.get(name=validated_data['current_name'])
    if 'new_name' in validated_data:
        category.name = validated_data['new_name']
    if 'is_active' in validated_data:
        category.is_active = validated_data['is_active']
    category.save()
    return category


def get_or_create_active_cart(user):
    cart, created = Cart.active.get_or_create(
        user=user,
        cart_status='O',
        is_active=True,
        defaults={'cart_status': 'O'}
    )
    return cart


def add_item_to_cart(cart, product_id, quantity):
    product = Product.active.get(id=product_id)
    cart_item, created = CartItem.active.get_or_create(
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

    # Check cart size before adding items to cart
    cart_products_count = cart.cartitem_set.aggregate(Sum('quantity'))['quantity__sum'] or 0
    if cart_products_count + len(items_data) > 10:
        raise TooManyItemsException()

    cart_items = []
    for item_data in items_data:
        cart_item = add_item_to_cart(cart, item_data['product_id'], item_data['quantity'])
        cart_items.append(cart_item)

    return cart, cart_items


def get_user_purchase_receipts(user, **filters):
    return PurchaseReceipt.active.filter(user=user)


def get_user_open_carts(user, **filters):
    return Cart.active.filter(user=user, cart_status='O')
