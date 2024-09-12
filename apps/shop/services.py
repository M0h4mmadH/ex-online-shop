from typing import Union

from apps.shop.models import Product, Post, Comment
from apps.user.models import User


def create_user_comment(*, user: User, comment: str, product_id: int, post: Union[Post, None]):
    product = Product.objects.get(id=product_id)
    Comment.objects.create(user=user, comment=comment, product=product, post=post)
