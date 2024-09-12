from typing import Union

from apps.shop.models import Product, Post, Comment, UserRateProduct
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
