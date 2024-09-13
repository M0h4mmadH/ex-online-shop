from django.db import models

from apps.user.models import User


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)


class City(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=True)
    price = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    discount = models.IntegerField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PurchaseReceipt(models.Model):
    items = models.ManyToManyField(Order, through='ReceiptOrder')
    price = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ReceiptOrder(models.Model):
    receipt = models.ForeignKey(PurchaseReceipt, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    CART_STATUS = (
        ('O', 'OPEN'),
        ('P', 'PAID'),
        ('E', 'EXPIRED'),
    )
    products = models.ManyToManyField(Product, through='CartItem')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    cart_status = models.CharField(max_length=1, choices=CART_STATUS, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, null=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)


class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    address = models.CharField(max_length=250, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return f"{str(self.city)} - {self.address}"


class Post(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    description = models.CharField(max_length=2500, null=False, blank=True)
    is_active = models.BooleanField(default=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    comment = models.CharField(max_length=2500, null=False, blank=True)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    is_active = models.BooleanField(default=True)


class UserRateProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    rate = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
