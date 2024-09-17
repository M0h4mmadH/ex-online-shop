from typing import Union
from django.db.models import Sum

from apps.shop.models import (Product, Post, Comment, UserRateProduct, Address, City, Cart)
from apps.user.models import User
from apps.utils.exceptions import EmptyCartException, UserCartAddressCityDoesNotMatch
from apps.utils.purchase_gateway import purchase_gateway


def create_user_comment(*, user: User, comment: str, product_id: int, post: Union[Post, None]):
    product = Product.active.get(id=product_id)
    Comment.objects.create(user=user, comment=comment, product=product, post=post)


def create_or_update_user_product_rate(*, user: User, product_id: int, rate: int):
    product = Product.active.get(id=product_id)
    previous_rate = UserRateProduct.objects.filter(user=user, product=product)
    if previous_rate.exists():
        previous_rate.delete()

    UserRateProduct.objects.create(user=user, product=product, rate=rate)


def create_user_address(*, user: User, city: str, address: str):
    city = City.active.get(name=city)
    return Address.objects.create(user=user, city=city, address=address)


def update_user_address(*, user: User, address_id: int, new_address: Union[str, None], new_city: Union[str, None]):
    address = Address.active.get(user=user, id=address_id)
    if new_city is not None:
        new_city = City.active.get(name=new_city)
        address.city = new_city

    if new_address is not None:
        address.address = new_address

    address.save()
    return address


def inactive_user_address(*, user: User, address_id: int):
    address = Address.active.get(user=user, id=address_id)
    address.is_active = False
    address.save()
    return address


def delete_user_cart(*, user: User, cart_id: int):
    cart = Cart.active.get(user=user, id=cart_id)
    cart.is_active = False
    return cart.save()


def user_purchase_order(*, user: User, cart_id: int, address_id: int):
    address = Address.active.get(user=user, id=address_id, is_active=True)
    cart = Cart.active.get(user=user, id=cart_id, is_active=True)
    products = cart.products.all()
    if len(products) == 0:
        raise EmptyCartException()

    for product in products:
        if product.city is None:
            continue
        if not product.city.id == address.city.id:
            raise UserCartAddressCityDoesNotMatch(product_id=product.id)

    total_price = products.aggregate(Sum('price'))['price__sum']
    tracking_code = purchase_gateway(total_price)
    cart.cart_status = 'P'
    cart.save()
    return cart, total_price, tracking_code
