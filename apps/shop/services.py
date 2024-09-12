from typing import Union

from apps.shop.models import (Product, Post, Comment, UserRateProduct, Address, City)
from apps.user.models import User


def create_user_comment(*, user: User, comment: str, product_id: int, post: Union[Post, None]):
    product = Product.objects.get(id=product_id)
    Comment.objects.create(user=user, comment=comment, product=product, post=post)


def create_or_update_user_product_rate(*, user: User, product_id: int, rate: int):
    product = Product.objects.get(id=product_id)
    previous_rate = UserRateProduct.objects.filter(user=user, product=product)
    if previous_rate.exists():
        previous_rate.delete()

    UserRateProduct.objects.create(user=user, product=product, rate=rate)


def create_user_address(*, user: User, city: str, address: str):
    city = City.objects.get(name=city)
    return Address.objects.create(user=user, city=city, address=address)


def update_user_address(*, user: User, address_id: int, new_address: Union[str, None], new_city: Union[str, None]):
    address = Address.objects.get(user=user, id=address_id)
    if new_city is not None:
        new_city = City.objects.get(name=new_city)
        address.city = new_city

    if new_address is not None:
        address.address = new_address

    address.save()
    return address


def inactive_user_address(*, user: User, address_id: int):
    address = Address.objects.get(user=user, id=address_id)
    address.is_active = False
    address.save()
    return address

