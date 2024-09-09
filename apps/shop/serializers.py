from rest_framework import serializers

from apps.shop.models import *


class InGetProducts(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    min_price = serializers.IntegerField(required=False, min_value=0)
    max_price = serializers.IntegerField(required=False, min_value=0)
    order_by = serializers.ChoiceField(choices=['name', 'price', '-name', '-price'], required=False)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name']


class OutGetProducts(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'created', 'updated', 'is_active']


class InGetCategories(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    order_by = serializers.ChoiceField(choices=['name', '-name'], required=False)


class OutGetCategories(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'is_active']


class InGetCategories(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True)
    order_by = serializers.ChoiceField(choices=['name', '-name'], required=False)


class OutGetCategories(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'is_active']


class InGetUserOrders(serializers.ModelSerializer):
    pass


class OutGetUserOrders(serializers.ModelSerializer):
    pass


class InGetUserCards(serializers.ModelSerializer):
    pass


class OutGetUserCards(serializers.ModelSerializer):
    pass


class InPurchaseOrders(serializers.ModelSerializer):
    pass


class OutPurchaseOrders(serializers.ModelSerializer):
    pass


class InAdminCreateProducts(serializers.ModelSerializer):
    pass


class OutAdminCreateProducts(serializers.ModelSerializer):
    pass


class InAdminUpdateProducts(serializers.ModelSerializer):
    pass


class OutAdminUpdateProducts(serializers.ModelSerializer):
    pass


class InSearchProducts(serializers.ModelSerializer):
    pass


class OutSearchProducts(serializers.ModelSerializer):
    pass


class InCommentProducts(serializers.ModelSerializer):
    pass


class OutCommentProducts(serializers.ModelSerializer):
    pass


class InUserAddAddress(serializers.ModelSerializer):
    pass


class OutUserAddAddress(serializers.ModelSerializer):
    pass


class InUserAddItemsToCard(serializers.ModelSerializer):
    pass


class OutUserAddItemsToCard(serializers.ModelSerializer):
    pass


class InUserDeleteAddress(serializers.ModelSerializer):
    pass


class OutUserDeleteAddress(serializers.ModelSerializer):
    pass
